import asyncio
import time
import curses


async def blink(canvas, row, column, symbol='*'):
    while True:
        canvas.addstr(row, column, symbol, curses.A_DIM)
        await asyncio.sleep(0)

        canvas.addstr(row, column, symbol)
        await asyncio.sleep(0)

        canvas.addstr(row, column, symbol, curses.A_BOLD)
        await asyncio.sleep(0)

        canvas.addstr(row, column, symbol)
        await asyncio.sleep(0)


def draw(canvas):
    row, column = (5, 20)
    set_of_stars = []
    for count in range(5):
        column += 5
        star = blink(canvas, row, column, symbol='*')
        set_of_stars.append(star)

        curses.curs_set(False)
        canvas.border()
    while True:
        for corutin in set_of_stars.copy():
            corutin.send(None)
            canvas.refresh()
    time.sleep(3)


if __name__ == '__main__':
    curses.update_lines_cols()
    curses.wrapper(draw)

