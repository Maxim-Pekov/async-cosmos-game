import time
import curses
import random
import asyncio
import fire_animation, curses_tools

from itertools import cycle


TIC_TIMEOUT = 5
BORDER_WIDTH = 2
NUMBER_OF_STARS = 50
FLICKER_BEAT = (20, 3, 5, 3)


async def blink(canvas, row, column, offset_tics, symbol='*'):

    while True:
        canvas.addstr(row, column, symbol, curses.A_DIM)
        for _ in range(FLICKER_BEAT[0]):
            await asyncio.sleep(0)

        canvas.addstr(row, column, symbol)
        for _ in range(FLICKER_BEAT[1]):
            await asyncio.sleep(0)

        canvas.addstr(row, column, symbol, curses.A_BOLD)
        for _ in range(FLICKER_BEAT[2]):
            await asyncio.sleep(0)

        canvas.addstr(row, column, symbol)
        for _ in range(FLICKER_BEAT[3]):
            await asyncio.sleep(0)

        for _ in range(offset_tics):
            await asyncio.sleep(0)


def draw_stars(canvas, window_height, window_width):
    set_of_stars = []
    stars_symbols = ['*', '+', ':', '.']
    for _ in range(NUMBER_OF_STARS):
        row = random.randint(BORDER_WIDTH, window_height - BORDER_WIDTH)
        column = random.randint(BORDER_WIDTH, window_width - BORDER_WIDTH)
        stars_symbol = random.choice(stars_symbols)
        offset_tics = random.randint(1, TIC_TIMEOUT)
        star = blink(canvas, row, column, offset_tics, symbol=stars_symbol)
        set_of_stars.append(star)
    return set_of_stars


async def animate_spaceship(canvas, window_height, window_width):
    with open("animations/rocket_frame_1.txt", "r") as my_file:
        frame1 = my_file.read()
    with open("animations/rocket_frame_2.txt", "r") as my_file:
        frame2 = my_file.read()
    rocket_height, rocket_width = curses_tools.get_frame_size(frame1)
    rocket_row_position = window_height - rocket_height - BORDER_WIDTH
    rocket_col_position = (window_width // 2) - BORDER_WIDTH

    for rocket_frame in cycle([frame1, frame2]):
        rows_direction, columns_direction, space_pressed = curses_tools.read_controls(
            canvas)
        rocket_row_position += rows_direction
        rocket_col_position += columns_direction

        rocket_row_position = max(BORDER_WIDTH / 2, rocket_row_position)
        rocket_col_position = max(BORDER_WIDTH / 2, rocket_col_position)
        rocket_row_position = min(
            rocket_row_position,
            window_height - rocket_height - BORDER_WIDTH / 2
        )
        rocket_col_position = min(
            rocket_col_position, window_width - rocket_width - BORDER_WIDTH / 2
        )

        curses_tools.draw_frame(
            canvas, rocket_row_position, rocket_col_position, rocket_frame
        )
        for _ in range(2):
            await asyncio.sleep(0)
        curses_tools.draw_frame(
            canvas, rocket_row_position, rocket_col_position, rocket_frame,
            negative=True
        )


def draw(canvas):
    curses.curs_set(False)
    canvas.nodelay(True)
    canvas.border()

    window_height, window_width = canvas.getmaxyx()

    coroutines = draw_stars(canvas, window_height, window_width)
    coroutines.append(
        fire_animation.fire(
            canvas,
            start_row=window_height - BORDER_WIDTH,
            start_column=window_width // 2
        )
    )
    coroutines.append(animate_spaceship(canvas, window_height, window_width))

    while True:
        for coroutine in coroutines.copy():
            try:
                coroutine.send(None)
            except StopIteration:
                coroutines.remove(coroutine)
            time.sleep(0.001)
        canvas.refresh()


def main():
    curses.update_lines_cols()
    curses.wrapper(draw)


if __name__ == '__main__':
    main()


