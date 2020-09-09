import requests
import bs4
import wikipedia
import re

def wiki_searching(text_msg):
    wikipedia.set_lang("RU")

    query = re.split("[, \-!?:]+", text_msg)
    querys = wikipedia.search("".join(query[1:]))
    if not querys:
        return "Ничего не найдено"
    else:
        html_page = requests.get('https://ru.wikipedia.org/wiki/{0}'.format(querys[0])).content
        soup = bs4.BeautifulSoup(html_page, features="html.parser")
        mw = soup.find('div', {'class', "mw-parser-output"}).find_all('p')
        return mw[0].text
