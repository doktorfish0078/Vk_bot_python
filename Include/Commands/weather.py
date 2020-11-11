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
    "Снег": "❄⛄❄"
}


def weather(tomorrow=False):
    time_day = ['Утром', 'Днём', 'Вечером', 'Ночью']
    numb_card_for_parsing = 0
    day = 'сегодня'
    if tomorrow:
        numb_card_for_parsing = 2
        day = 'завтра'
    try:
        html_text = requests.get('https://yandex.ru/pogoda/izhevsk/details?via=ms').text
        soup = BeautifulSoup(html_text, features="html.parser")
        weather = soup.find_all('div', {'class', 'card'})

        weather_condition = weather[numb_card_for_parsing].find_all('td', {'class',
                                                                           'weather-table__body-cell weather-table__body-cell_type_condition'})

        temp = weather[numb_card_for_parsing].find_all('div', {'class', 'weather-table__temp'})

        temp_feels_like = weather[numb_card_for_parsing].find_all('td', {'class',
                                                                         'weather-table__body-cell weather-table__body-cell_type_feels-like'})

        result_weather = ['Погода на {}:\n'.format(day), weather_condition[2].text]

        for day in range(len(time_day)):
            result_weather[0] += "{0} {1}, {2}{3}, ощущается как {4}\n".format(
                time_day[day], temp[day].text, weather_condition[day].text,
                weather_type[weather_condition[day].text], temp_feels_like[day].text)
        return result_weather

    except BaseException:
        print("Error weather")
        return ("Не удалось получить погоду :(", "Err")


print(weather())
