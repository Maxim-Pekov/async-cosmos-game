import asyncio
import time
import curses
import random
import fire_animation, curses_tools


with open("animations/rocket_frame_1.txt", "r") as my_file:
    file_contents = my_file.read()
with open("animations/rocket_frame_2.txt", "r") as my_file:
    file_contents2 = my_file.read()
frame1 = f'''{file_contents}'''
frame2 = f'''{file_contents2}'''


async def blink(canvas, row, column, symbol='*'):
    while True:
        canvas.addstr(row, column, symbol, curses.A_DIM)
        await asyncio.sleep(0)
        time.sleep(0.02)

        canvas.addstr(row, column, symbol)
        await asyncio.sleep(0)
        time.sleep(0.003)

        canvas.addstr(row, column, symbol, curses.A_BOLD)
        await asyncio.sleep(0)
        time.sleep(0.005)

        canvas.addstr(row, column, symbol)
        await asyncio.sleep(0)
        time.sleep(0.0001)


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


async def animate_spaceship(canvas, window_height, window_width):
    while True:
        curses_tools.draw_frame(
            canvas, window_height - 11, (window_width // 2) - 2, frame1
        )
        time.sleep(0.3)
        await asyncio.sleep(0)
        curses_tools.draw_frame(
            canvas, window_height - 11,
            (window_width // 2) - 2,
            frame1, negative=True
        )
        curses_tools.draw_frame(
            canvas, window_height - 11, (window_width // 2)- 2, frame2
        )
        time.sleep(0.3)
        await asyncio.sleep(0)
        curses_tools.draw_frame(
            canvas, window_height - 11, (window_width // 2) - 2,
            frame2, negative=True
        )


def draw(canvas):
    window_height, window_width = (curses.LINES, curses.COLS)
    coroutines = draw_stars(canvas, window_height, window_width)
    coroutines.append(fire_animation.fire(canvas, start_row=window_height - 2, start_column=window_width // 2))
    coroutines.append(animate_spaceship(canvas, window_height, window_width))


    while True:
        for coroutine in coroutines.copy():
            try:
                coroutine.send(None)
            except StopIteration:
                coroutines.remove(coroutine)
            curses.curs_set(False)
            canvas.border()
            canvas.refresh()
        if len(coroutines) == 0:
            break


if __name__ == '__main__':
    curses.update_lines_cols()
    curses.wrapper(draw)



