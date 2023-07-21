from curses_tools import draw_frame, get_frame_size
from obstacles  import Obstacle, show_obstacles
import asyncio


def get_random_frame(random_frame):
    with open(f"animations/garbages/{random_frame}", "r") as garbage_file:
        frame = garbage_file.read()
    return frame


async def fly_garbage(canvas, column, garbage_frame, obstacles, coroutines, speed=0.5):
    """Animate garbage, flying from top to bottom. Сolumn position will stay same, as specified on start."""
    rows_number, columns_number = canvas.getmaxyx()

    column = max(column, 0)
    column = min(column, columns_number - 1)

    row = 0

    frame_height, frame_width = get_frame_size(garbage_frame)
    obstacle = Obstacle(row, column, frame_height, frame_width)
    obstacles.append(obstacle)

    while row < rows_number:
        draw_frame(canvas, row, column, garbage_frame)
        await asyncio.sleep(0)
        draw_frame(canvas, row, column, garbage_frame, negative=True)
        row += speed
        obstacle.row += speed
    await asyncio.sleep(0)

    obstacles.remove(obstacle)

