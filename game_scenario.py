import asyncio

from curses_tools import draw_frame
from fire_animation import get_hits


year = 1957


async def sleep(tics=1):
    for _ in range(tics):
        await asyncio.sleep(0)


PHRASES = {
    1957: "First Sputnik",
    1961: "Gagarin flew!",
    1969: "Armstrong got on the moon!",
    1971: "First orbital space station Salute-1",
    1981: "Flight of the Shuttle Columbia",
    1998: 'ISS start building',
    2011: 'Messenger launch to Mercury',
    2020: "Take the plasma gun! Shoot the garbage!",
}

def get_garbage_delay_tics():
    global year
    if year < 1961:
        return None
    elif year < 1969:
        return 20
    elif year < 1981:
        return 14
    elif year < 1995:
        return 10
    elif year < 2010:
        return 8
    elif year < 2020:
        return 6
    else:
        return 2


def get_year():
    return year

async def count_years():
    global year
    while True:
        year += 1
        await sleep(10)


async def show_count_years(canvas):
    global year
    rows_number, columns_number = canvas.getmaxyx()

    while True:
        if year in PHRASES:
            year_text = f'{year}: {PHRASES[year]}'
        else:
            year_text = str(year)
        draw_frame(canvas, rows_number - 2, 2, year_text)
        draw_frame(canvas, rows_number - 2, columns_number - 12, 'Score:' + str(get_hits()))

        await sleep(10)
        draw_frame(canvas, rows_number - 2, 2, year_text, negative=True)
        draw_frame(canvas, rows_number - 2, columns_number - 12, 'Score:' + str(get_hits()), negative=True)
