import random
import bs4
import re
import requests


def get_films():
    result = ''
    try:
        html_page1 = requests.get('https://www.kinoafisha.info/rating/movies/?page=0').text
        html_page2 = requests.get('https://www.kinoafisha.info/rating/movies/?page=1').text
        soup = bs4.BeautifulSoup(html_page1 + html_page2, features="html.parser")
        films_name = soup.find_all('a', {'class' : 'films_name ref'})
        about_films = soup.find_all('span', {'class' : 'films_info'})

        films = []
        rand_nmbs = [random.randint(0, len(films_name)),random.randint(0, len(films_name)),random.randint(0, len(films_name))]

        # for i in range(len(films_name)):
        #     films.append("{} | {}, {}, режиссёр:{}".format(films_name[i].text, about_films[i*3].text,
        #                                                    about_films[i * 3 + 1].text,  re.sub(r'\s+', ' ', about_films[i * 3 + 2].text )))
        #А вот тут в 23:54 11.09 Я задался вопросом, зачем мы все фильмы переводим в текстовый вариант,если нам нужно только 3 рандомных?! Это же лишнее время

        for i in rand_nmbs:
            films.append("Фильм: {} | {} | Жанр: {} | Режиссёр:{}".format(films_name[i].text, about_films[i * 3].text,
                                                           about_films[i * 3 + 1].text,
                                                           re.sub(r'\s+', ' ', about_films[i * 3 + 2].text)))

        # for pp in rand_nmbs:
        #     result += 'Фильм: ' + films[pp] + '\n'

        return "\n".join(films)
    except BaseException:
        return "Не удалось получить фильмы :("

print(get_films())