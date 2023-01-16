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
    star = blink(canvas, row, column, symbol='*')
    curses.curs_set(False)
    canvas.border()
    while True:
        star.send(None)
        canvas.refresh()
    time.sleep(3)


if __name__ == '__main__':
    curses.update_lines_cols()
    curses.wrapper(draw)

