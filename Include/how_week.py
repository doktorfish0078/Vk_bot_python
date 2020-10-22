from Head import current_datetime
from datetime import date

def how_week():
    now = current_datetime()

    print(now)

    week_num = date(now.year, now.month, now.day).isocalendar()[1]

    if week_num%2 == 0:
        return '⏫⬆️ Неделя над чертой ⬆️⏫'
    return '⏬⬇️ Неделя под чертой ⬇️⏬'
