import time
import curses


def draw(canvas):
    while True:
        row, column = (5, 20)
        curses.curs_set(False)
        canvas.border()

        canvas.addstr(row, column, '*', curses.A_DIM)
        time.sleep(2)
        canvas.refresh()

        canvas.addstr(row, column, '*')
        time.sleep(0.3)
        canvas.refresh()

        canvas.addstr(row, column, '*', curses.A_BOLD)
        time.sleep(0.5)
        canvas.refresh()

        canvas.addstr(row, column, '*')
        time.sleep(0.3)
        canvas.refresh()


if __name__ == '__main__':
    curses.update_lines_cols()
    curses.wrapper(draw)

