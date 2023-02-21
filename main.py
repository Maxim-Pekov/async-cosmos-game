import asyncio
from itertools import cycle
import time
import curses
import random
import fire_animation, curses_tools


TIC_TIMEOUT = 0.1
BORDER_WIDTH = 2
ROCKET_HEIGHT = 9
ROCKET_WIDTH = 5


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
        row = random.randint(BORDER_WIDTH, window_height - BORDER_WIDTH)
        column = random.randint(BORDER_WIDTH, window_width - BORDER_WIDTH)
        stars_symbol = random.choice(stars_symbols)
        star = blink(canvas, row, column, symbol=stars_symbol)
        set_of_stars.append(star)
    return set_of_stars


async def animate_spaceship(canvas, row, col, window_height, window_width):
    with open("animations/rocket_frame_1.txt", "r") as my_file:
        frame1 = my_file.read()
    with open("animations/rocket_frame_2.txt", "r") as my_file:
        frame2 = my_file.read()

    for rocket_frame in cycle([frame1, frame2]):
        rows_direction, columns_direction, space_pressed = curses_tools.read_controls(
            canvas)
        row += rows_direction
        col += columns_direction

        row = max(1, row)
        col = max(1, col)
        row = min(row, window_height - ROCKET_HEIGHT / 2)
        col = min(col, window_width - ROCKET_WIDTH - BORDER_WIDTH / 2)

        curses_tools.draw_frame(canvas, row, col, rocket_frame)
        await asyncio.sleep(0)
        curses_tools.draw_frame(
            canvas, row,
            col,
            rocket_frame, negative=True
        )


def draw(canvas):
    window_height, window_width = canvas.getmaxyx()
    row = window_height - ROCKET_HEIGHT - BORDER_WIDTH
    col = (window_width // 2) - BORDER_WIDTH

    coroutines = draw_stars(canvas, window_height, window_width)
    coroutines.append(
        fire_animation.fire(
            canvas,
            start_row=window_height - BORDER_WIDTH,
            start_column=window_width // 2
        )
    )
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


def main():

    curses.update_lines_cols()
    curses.wrapper(draw)

if __name__ == '__main__':
    main()


