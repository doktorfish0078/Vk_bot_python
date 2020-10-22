import requests
import random
from bs4 import BeautifulSoup


def get_top():
    anime = []
    url = 'https://you-anime.ru/top-anime'
    try:
        html_text = requests.get(url)
        soup = BeautifulSoup(html_text.text, features="html.parser")
        items = soup.find_all('div', {'class', 'item'})

        rand_nmbs = [random.randint(0, len(items)), random.randint(0, len(items)),
                     random.randint(0, len(items))]

        for i in rand_nmbs:
            name = items[i].find('a', {'class', 'name'})
            href = url + items[i].find('a')['href']

            anime.append("Аниме: {}, Ссылка: {}".format(name.text, href))

        return "\n".join(anime)
    except BaseException:
        return "Не удалось получить анимешечки :("
