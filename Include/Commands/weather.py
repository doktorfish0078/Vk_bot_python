import requests
from bs4 import BeautifulSoup


parts = ['morning','day','evening','night']
url = 'https://api.weather.yandex.ru/v2/forecast?'
api_key_yandex = 'c585325e-939a-4e62-bfb1-af081d21f2ea'
lat=56.86186
lon=53.23243
headers = {
    'X-Yandex-API-Key': 'c585325e-939a-4e62-bfb1-af081d21f2ea'
}
params = {
    'lat': 'lat',
    'lon': 'lon'
}


def weather_td():
    timeday = ['Утром ', 'Днём ', 'Вечером ', 'Ночью ']

    try:
        out_weather = 'Погода на сегодня:\n'
        html_text = requests.get('https://yandex.ru/pogoda/izhevsk/details?via=ms').text
        soup = BeautifulSoup(html_text, features="html.parser")
        weather = soup.find_all('div', {'class', 'card'})
        temp = weather[0].find_all('span', {'class', 'temp__value'})
        for day in range(len(timeday)):
            for i in range(day * 3,(day + 1) * 3):
                if day * 3 + 1 == i:
                    timeday[day] += '...'
                elif day * 3 + 2 == i:
                    timeday[day] += ' ощущается как '
                timeday[day] += temp[i].text + 'ºC'
            out_weather += timeday[day] + '\n'
        return out_weather
    except BaseException:
        return 'pezda pogode'


def weather_tm():
    timeday = ['Утром ', 'Днём ', 'Вечером ', 'Ночью ']

    try:
        out_weather = 'Погода на завтра:\n'
        html_text = requests.get('https://yandex.ru/pogoda/izhevsk/details?via=ms').text
        soup = BeautifulSoup(html_text, features="html.parser")
        weather = soup.find_all('div', {'class', 'card'})
        temp = weather[2].find_all('span', {'class', 'temp__value'})
        for day in range(len(timeday)):
            for i in range(day * 3,(day + 1) * 3):
                if day * 3 + 1 == i:
                    timeday[day] += '...'
                elif day * 3 + 2 == i:
                    timeday[day] += ' ощущается как '
                timeday[day] += temp[i].text + 'ºC'
            out_weather += timeday[day] + '\n'
        return out_weather
    except BaseException:
        return 'pezda pogode'


def weater_api_yandx_today():
    out_weather = 'Погода на сегодня:\n'
    try:
        html_text = requests.get(url,params=params,headers = headers).json()
        for part in parts:
            temp_min = html_text['forecasts'][0]['parts'][part]['temp_min']
            temp_max = html_text['forecasts'][0]['parts'][part]['temp_max']
            feels_like = html_text['forecasts'][0]['parts'][part]['feels_like']
            f = '{0} {1}ºC...{2}ºC feels like {3}ºC\n'.format(part, temp_min, temp_max, feels_like)
            out_weather += f
        return out_weather
    except BaseException:
        return 'Gabela'


def weater_api_yandx_tomorrow():
    out_weather = 'Погода на завтра:\n'
    try:
        html_text = requests.get(url,params=params,headers = headers).json()
        for part in parts:
            temp_min = html_text['forecasts'][1]['parts'][part]['temp_min']
            temp_max = html_text['forecasts'][1]['parts'][part]['temp_max']
            feels_like = html_text['forecasts'][1]['parts'][part]['feels_like']
            f = '{0} {1}ºC...{2}ºC feels like {3}ºC\n'.format(part,temp_min,temp_max,feels_like)
            out_weather += f
        return out_weather
    except BaseException:
        return 'Gabela'
