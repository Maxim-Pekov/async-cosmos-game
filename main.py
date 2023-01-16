import asyncio
import random
import time
import curses


SLEEP_TIME = random.randint(1, 10)


async def blink(canvas, row, column, symbol='*'):
    while True:
        time.sleep(SLEEP_TIME/250)

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

        time.sleep(SLEEP_TIME / 250)




def draw(canvas):
    window_height, window_width = (curses.LINES, curses.COLS)

    set_of_stars = []
    stars_symbols = ['*', '+', ':', '.']

    for _ in range(50):
        row = random.randint(2, window_height - 2)
        column = random.randint(2, window_width - 2)
        stars_symbol = random.choice(stars_symbols)
        star = blink(canvas, row, column, symbol=stars_symbol)
        set_of_stars.append(star)

        curses.curs_set(False)
        canvas.border()
    while True:
        for corutin in set_of_stars.copy():
            corutin.send(None)
            canvas.refresh()
    time.sleep(SLEEP_TIME / 100)


if __name__ == '__main__':
    curses.update_lines_cols()
    curses.wrapper(draw)

