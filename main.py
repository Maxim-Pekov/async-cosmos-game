import asyncio
import random
import time
import curses
import fire_animation


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

    coroutines = []
    stars_symbols = ['*', '+', ':', '.']

    for _ in range(50):
        row = random.randint(2, window_height - 2)
        column = random.randint(2, window_width - 2)
        stars_symbol = random.choice(stars_symbols)
        star_coroutines = blink(canvas, row, column, symbol=stars_symbol)
        coroutines.append(star_coroutines)



        curses.curs_set(False)
        canvas.border()
        fire_coroutine = fire_animation.fire(
            canvas, start_row=window_height - 2, start_column=window_width // 2
        )
        coroutines.append(fire_coroutine)

    while True:

        # try:
        #     fire_coroutine.send(None)
        #     canvas.refresh()
        # except StopIteration:
        #     break

        for coroutine in coroutines.copy():
            try:
                coroutine.send(None)
                canvas.refresh()
            except StopIteration:
                coroutines.remove(coroutine)
        if len(coroutines) == 0:
            break







    time.sleep(SLEEP_TIME / 100)


if __name__ == '__main__':
    curses.update_lines_cols()
    curses.wrapper(draw)

