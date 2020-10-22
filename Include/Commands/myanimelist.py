import requests
import random
from bs4 import BeautifulSoup

def rearm_unused():
    global unused
    unused = [i for i in range(100)]


rearm_unused()


def get_top():
    anime = []
    url = 'https://you-anime.ru/top-anime'
    try:
        html_text = requests.get(url)
        soup = BeautifulSoup(html_text.text, features="html.parser")
        items = soup.find_all('div', {'class', 'item'})

        rand_nmbs = [unused.pop(random.randint(0, len(unused)-1)),
                     unused.pop(random.randint(0, len(unused)-1)),
                     unused.pop(random.randint(0, len(unused))-1)]

        if len(unused) < 3:
            rearm_unused()

        for i in rand_nmbs:
            name = items[i].find('a', {'class', 'name'})
            href = "https://you-anime.ru/" + items[i].find('a')['href']
            anime.append("Аниме: {}, Ссылка: {}".format(name.text, href))

        return "\n".join(anime)
    except BaseException:
        return "Не удалось получить анимешечки :("


def get_all():
    anime = []
    try:
        for i in range(3):
            url = 'https://you-anime.ru/filter?page={}'.format(random.randint(1, 40))
            html_text = requests.get(url)
            soup = BeautifulSoup(html_text.text, features="html.parser")
            items = soup.find_all('div', {'class', 'item'})

            anime_from_page = random.randint(0, 30)

            name = items[anime_from_page].find('a', {'class', 'name'})
            href = "https://you-anime.ru/" + items[anime_from_page].find('a')['href']
            anime.append("Аниме: {}, Ссылка: {}".format(name.text, href))

        return "\n".join(anime)
    except BaseException:
        return "Не удалось получить анимешечки :("
