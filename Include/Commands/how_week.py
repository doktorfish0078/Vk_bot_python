from datetime import date, datetime


def how_week():
    now = datetime.now()

    week_num = date(now.year, now.month, now.day).isocalendar()[1]
    if week_num%2 == 0:
        return '⤊↾⇯⇈⟰⥠⥜ Неделя над чертой ⇑↑⇡⬆︎⥘⇫⤒⇞'
    return '⇩⥝⥙↯⇊⤋ Неделя под чертой ↧⥡⇃↓⥡⤈'
