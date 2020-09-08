import requests
from bs4 import BeautifulSoup


def weather(tomorrow = False):
    timeday = ['Утром ', 'Днём ', 'Вечером ', 'Ночью ']
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
        out_weather = ['Погода на {}:\n'.format(day), weather_condition[2].text]
        temp = weather[numb_card_for_parsing].find_all('span', {'class', 'temp__value'})
        for day in range(len(timeday)):
            timeday[day] += '{} '.format(weather_condition[day].text)
            for i in range(day * 3, (day + 1) * 3):
                if day * 3 + 1 == i:
                    timeday[day] += '...'
                elif day * 3 + 2 == i:
                    timeday[day] += ' ощущается как '
                timeday[day] += temp[i].text + 'ºC'
            out_weather[0] += timeday[day] + '\n'
        return out_weather
    except BaseException:
        return 'pezda pogode'

