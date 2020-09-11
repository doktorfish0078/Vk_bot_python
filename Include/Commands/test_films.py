import random
import bs4
import re
import requests


def get_films():
    result = ''
    html_page = requests.get('https://www.kinoafisha.info/rating/movies/?page=0').text
    soup = bs4.BeautifulSoup(html_page, features="html.parser")
    films_name = soup.find_all('a', {'class' : 'films_name ref'})
    about_films = soup.find_all('span', {'class' : 'films_info'})

    films = []
    rand_nmbs = [random.randint(0, len(films_name)),random.randint(0, len(films_name)),random.randint(0, len(films_name))]

    for i in range(len(films_name)):
        films.append("{} | {}, {}, режиссёр:{}".format(films_name[i].text, about_films[i*3].text,
                                                       about_films[i * 3 + 1].text,  re.sub(r'\s+', ' ', about_films[i * 3 + 2].text )))


    for pp in rand_nmbs:
        result += 'Фильм: ' + films[pp] + '\n'

    return result


