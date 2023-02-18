import asyncio
import time
import curses
import random
import fire_animation, curses_tools


TIC_TIMEOUT = 0.1


with open("animations/rocket_frame_1.txt", "r") as my_file:
    frame1 = my_file.read()
with open("animations/rocket_frame_2.txt", "r") as my_file:
    frame2 = my_file.read()


async def blink(canvas, row, column, symbol='*'):
    while True:
        canvas.addstr(row, column, symbol, curses.A_DIM)
        for _ in range(20):
            await asyncio.sleep(0)

        canvas.addstr(row, column, symbol)
        for _ in range(3):
            await asyncio.sleep(0)

        canvas.addstr(row, column, symbol, curses.A_BOLD)
        for _ in range(5):
            await asyncio.sleep(0)

        canvas.addstr(row, column, symbol)
        for _ in range(3):
            await asyncio.sleep(0)

        x = random.randint(1, 10)
        for _ in range(x):
            await asyncio.sleep(0)


def draw_stars(canvas, window_height, window_width):
    set_of_stars = []
    stars_symbols = ['*', '+', ':', '.']
    for _ in range(50):
        row = random.randint(2, window_height - 2)
        column = random.randint(2, window_width - 2)
        stars_symbol = random.choice(stars_symbols)
        star = blink(canvas, row, column, symbol=stars_symbol)
        set_of_stars.append(star)
    return set_of_stars


async def animate_spaceship(canvas, row, col, window_height, window_width):

    while True:
        rows_direction, columns_direction, space_pressed = curses_tools.read_controls(
            canvas)
        row += rows_direction
        col += columns_direction

        if col <= -1:
            col = -1
        elif col >= window_width - 4:
            col = window_width - 4
        if row <= 0:
            row = 0
        elif row >= window_height - 2:
            row = window_height - 2

        curses_tools.draw_frame(
            canvas, row, col, frame1
        )
        await asyncio.sleep(0)
        curses_tools.draw_frame(
            canvas, row,
            col,
            frame1, negative=True
        )

        curses_tools.draw_frame(
            canvas, row, col, frame2
        )
        await asyncio.sleep(0)
        curses_tools.draw_frame(
            canvas, row, col,
            frame2, negative=True
        )


def draw(canvas):
    window_height, window_width = (curses.LINES, curses.COLS)
    row = window_height - 11
    col = (window_width // 2) - 2

    coroutines = draw_stars(canvas, window_height, window_width)
    coroutines.append(fire_animation.fire(canvas, start_row=window_height - 2, start_column=window_width // 2))
    coroutines.append(animate_spaceship(canvas, row, col, window_height, window_width))


    while True:
        for coroutine in coroutines.copy():
            try:
                coroutine.send(None)
            except StopIteration:
                coroutines.remove(coroutine)
            curses.curs_set(False)
            canvas.border()
            canvas.nodelay(True)
            canvas.refresh()
            time.sleep(0.001)
        if len(coroutines) == 0:
            break


if __name__ == '__main__':
    curses.update_lines_cols()
    curses.wrapper(draw)



