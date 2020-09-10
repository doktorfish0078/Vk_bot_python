import requests
import bs4
import wikipedia
import re


def wiki_searching(text_msg):
    wikipedia.set_lang("RU")

    text_query = re.split("[, \-!?:]+", text_msg)
    variant_query_from_wiki = wikipedia.search(" ".join(text_query[1:]))

    if not variant_query_from_wiki:
        return "Ничего не найдено"
    else:
        try:
            html_page = requests.get('https://ru.wikipedia.org/wiki/{0}'.format(variant_query_from_wiki[0])).content
            soup = bs4.BeautifulSoup(html_page, features="html.parser")
            parsed_graph = soup.find('div', {'class', "mw-parser-output"}).find_all('p')
            print(parsed_graph[0].text)
        except BaseException:
            return "Страница не найдена"




