import os
import time
import curses
import random
import asyncio
import fire_animation, curses_tools

from space_garbage import fly_garbage, get_random_frame
from itertools import cycle
from physics import update_speed
from show_gameover import show_game_over
from game_scenario import count_years, show_count_years, get_garbage_delay_tics, get_year
from obstacles import show_obstacles


coroutines = []
obstacles = []

DEBUG = False
TIC_TIMEOUT = 5
TIC_GARBAGE_TIMEOUT = 25
BORDER_WIDTH = 2
NUMBER_OF_STARS = 50
FLICKER_BEAT = (20, 3, 5, 3)
GUN_YEAR = 2020


async def sleep(tics=1):
    for _ in range(tics):
        await asyncio.sleep(0)


async def blink(canvas, row, column, offset_tics, symbol='*'):

    while True:
        canvas.addstr(row, column, symbol, curses.A_DIM)
        await sleep(FLICKER_BEAT[0])

        canvas.addstr(row, column, symbol)
        await sleep(FLICKER_BEAT[1])

        canvas.addstr(row, column, symbol, curses.A_BOLD)
        await sleep(FLICKER_BEAT[2])

        canvas.addstr(row, column, symbol)
        await sleep(FLICKER_BEAT[3])

        await sleep(offset_tics)


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
    global coroutines
    with open("animations/rocket_frame_1.txt", "r") as my_file:
        frame1 = my_file.read()
    with open("animations/rocket_frame_2.txt", "r") as my_file:
        frame2 = my_file.read()
    row_speed = column_speed = 0
    rocket_height, rocket_width = curses_tools.get_frame_size(frame1)
    rocket_row_position = window_height - rocket_height - BORDER_WIDTH
    rocket_col_position = (window_width // 2) - BORDER_WIDTH

    for rocket_frame in cycle([frame1, frame1, frame2, frame2]):
        rows_direction, columns_direction, space_pressed = curses_tools.read_controls(
            canvas)

        row_speed, column_speed = update_speed(
            row_speed, column_speed, rows_direction, columns_direction
        )
        rocket_row_position += row_speed
        rocket_col_position += column_speed

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
        await sleep(1)
        curses_tools.draw_frame(
            canvas, rocket_row_position, rocket_col_position, rocket_frame,
            negative=True
        )

        if space_pressed and get_year() > GUN_YEAR:
            coroutines.append(fire_animation.fire(
                canvas,
                obstacles,
                start_row=window_height - BORDER_WIDTH - rocket_height -1,
                start_column=rocket_col_position + rocket_width / 2 - 0.5
            ))

        for obstacle in obstacles:
            if obstacle.has_collision(rocket_row_position, rocket_col_position, rocket_height, rocket_width):
                coroutines.append(show_game_over(canvas))
                return

async def fill_orbit_with_garbage(canvas, window_width):
    global coroutines

    frames = os.listdir("animations/garbages")

    while True:
        random_frame = random.choice(frames)
        frame = get_random_frame(random_frame)
        if get_garbage_delay_tics():
            column = random.randint(BORDER_WIDTH, window_width - BORDER_WIDTH)
            offset_tics = get_garbage_delay_tics()
        else:
            column = None
            offset_tics = TIC_GARBAGE_TIMEOUT
        coroutines.append(fly_garbage(canvas, column, frame, obstacles))
        if DEBUG:
            coroutines.append(show_obstacles(canvas, obstacles))
        await sleep(offset_tics)



def draw(canvas):
    curses.curs_set(False)
    canvas.nodelay(True)
    canvas.derwin(5, 5)
    global coroutines

    window_height, window_width = canvas.getmaxyx()

    coroutines = draw_stars(canvas, window_height, window_width)
    coroutines.append(animate_spaceship(canvas, window_height, window_width))
    coroutines.append(count_years())
    coroutines.append(show_count_years(canvas))
    coroutines.append(fill_orbit_with_garbage(canvas, window_width))

    while True:
        canvas.border()


        for coroutine in coroutines.copy():
            try:
                coroutine.send(None)
            except StopIteration:
                coroutines.remove(coroutine)
        canvas.refresh()
        time.sleep(0.05)


def main():
    curses.update_lines_cols()
    curses.wrapper(draw)


if __name__ == '__main__':
    main()


