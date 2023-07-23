import asyncio

from curses_tools import draw_frame, get_frame_size
from fire_animation import get_hits


async def show_game_over(canvas):
    """If spaceship explose, show gameover"""

    with open("animations/game_over.txt", "r") as my_file:
        frame_game_over = my_file.read()

    rows_number, columns_number = canvas.getmaxyx()
    frame_height, frame_width = get_frame_size(frame_game_over)
    while True:
        draw_frame(canvas, rows_number / 2 - frame_height / 2, columns_number / 2 - frame_width / 2, frame_game_over)
        draw_frame(canvas, rows_number / 2 + frame_height / 2, columns_number / 2 - 6, f'YOUR SCORE: {get_hits()}')

        await asyncio.sleep(0)

