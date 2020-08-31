import requests
import bs4


def get_top(count: int=5, by: str="") -> dict:
    types = ["", "airing", "upcoming", "tv", "movie", "ova", "special", "bypopularity", "favorite"]
    if by not in types:
        return {"error: ": "Неизвестный тип!"}
    html = requests.get("https://myanimelist.net/topanime.php?type={0}".format(by))
    soup = bs4.BeautifulSoup(html.text, "html.parser")

    top = {}

    for anime in soup.select(".ranking-list", limit=count):

        url = anime.select(".hoverinfo_trigger")[0]['href']
        anime = anime.select(".hoverinfo_trigger")[0].findAll("img")[0]
        name = anime['alt'].split(":")[1].strip(" ")
        top[name] = url

    res = ""
    for anime in top:
        res += anime + " : " + top[anime] + "\n"
    return res


