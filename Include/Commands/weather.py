import requests
from bs4 import BeautifulSoup

weather_type = {
    "Пасмурно": "☁️☁️☁️",
    "Ясно": "☀️",
    "Облачно": "☁️",
    "Облачно с прояснениями": "⛅️",
    "Небольшой дождь": "🌧",
    "Дождь": "🌧☔️🌧",
    "Малооблачно": "🌤",
    "Небольшой снег": "❄",
    "Снег": "❄⛄❄",
    "Дождь со снегом": "🌧❄🌧"
}


def weather(tomorrow=False, week=False):
    time_day = ['Утром', 'Днём', 'Вечером', 'Ночью']
    numb_card_for_parsing = [0]
    day = 'сегодня'

    if tomorrow:
        numb_card_for_parsing = [2]
        day = 'завтра'

    if week:
        numb_card_for_parsing = [0, 2, 3, 4, 5, 6, 7, 8]
        day = 'неделю'

    try:
        html_text = requests.get('https://yandex.ru/pogoda/izhevsk/details?via=ms').text
        soup = BeautifulSoup(html_text, features="html.parser")
        weather_soup = soup.find_all('div', {'class', 'card'})

        result_weather = ['Погода на {}:\n'.format(day), '']

        for card in numb_card_for_parsing:

            weather_condition = weather_soup[card].find_all('td', {'class', 'weather-table__body-cell weather-table__body-cell_type_condition'})

            temp = weather_soup[card].find_all('div', {'class', 'weather-table__temp'})

            temp_feels_like = weather_soup[card].find_all('td', {'class', 'weather-table__body-cell weather-table__body-cell_type_feels-like'})

            date = '{} {}\n'.format(
                weather_soup[card].find('strong', {'class', 'forecast-details__day-number'}).text,
                weather_soup[card].find('span', {'class', 'forecast-details__day-month'}).text)

            result_weather[0] += date
            result_weather[1] = weather_condition[2].text
            for day in range(len(time_day)):
                result_weather[0] += "{0} {1}, {2}{3}, ощущается как {4}\n".format(
                    time_day[day], temp[day].text, weather_condition[day].text,
                    weather_type[weather_condition[day].text], temp_feels_like[day].text)
            result_weather[0] += '\n'
        return result_weather

    except BaseException:
        print("Error weather")
        return ("Не удалось получить погоду :(", "Err")
