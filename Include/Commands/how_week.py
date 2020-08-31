import requests
from bs4 import BeautifulSoup

def how_week():
    try:
        html_text = requests.get('https://istu.ru').text
        soup = BeautifulSoup(html_text, features="html.parser")
        week = soup.find('div', {'class': 'site-header-top-element ref-week type-separated'}).find('span').text
        return week
    except BaseException:
        return 'Не удалось получить информацию о неделе'
