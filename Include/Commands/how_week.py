from datetime import date, datetime, timedelta


def how_week():
    now = datetime.now() + timedelta(hours=4)

    print(now)

    week_num = date(now.year, now.month, now.day).isocalendar()[1]

    if week_num%2 == 0:
        return '⏫⬆️ Неделя над чертой ⬆️⏫'
    return '⏬⬇️ Неделя под чертой ⬇️⏬'
