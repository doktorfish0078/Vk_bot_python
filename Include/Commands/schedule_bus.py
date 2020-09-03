from selenium import webdriver
from selenium.webdriver.chrome.options import Options

import datetime
import re
import os


def get_path_schedule_bus(text_msg):
    """
    :param text_msg:
    :return: Возвращает путь до сделанного скриншота
    """
    path_to_chromdriver = ""
    now = datetime.datetime.now()  # текущая дата и время
    URL = "https://igis.ru/gortrans/bus/izh/"  # izh/номер автобуса
    numb_bus = get_numb_bus(text_msg)
    if numb_bus is None and 2 <= numb_bus <= 400:
        return None
    URL += numb_bus
    print(URL)


    #chrome_options = Options()
    #chrome_options.add_argument("--headless")
    #driver = webdriver.Chrome(options=chrome_options)
    #firefox_binary = os.environ.get('FIREFOX_BIN', None)
    #opt = webdriver.FirefoxOptions()
    #opt.add_argument("--headless")
    #driver = webdriver.Firefox(options=opt)
    #driver.set_window_size(1600, 2070)
    #driver.get(URL)
    #elem = driver.find_element_by_class_name("table-st1")
    #elem.screenshot(
    #    "screenshots\screen_" + now.strftime("%d-%m-%Y %H-%M-%S") + ".png")
    #driver.quit()
    #return "screenshots\screen_{0}.png".format(
       # now.strftime("%d-%m-%Y %H-%M-%S"))
        #print("Ошибка получения скриншота с адреса " + URL)
        #return "None"


def get_numb_bus(text_msg):
    """
    Парсит сообщения,ищя слово "автобус" и проверяя стоящие до и после него слово
    :param text_msg: Подаётся в низком регистре и только если есть в наличии слова "автобус" или "автобуса"
    :return: Цифру автобуса,если она есть. Если нет,возвращает None
    """
    words = re.split("[, \-!?:]+", text_msg)
    if "автобус" in words:
        index_bus = words.index("автобус")
    elif "автобуса" in words:
        index_bus = words.index("автобуса")

    if index_bus > 0 and words[index_bus - 1].isdigit():  # проверяем слово перед автобусом
        return words[index_bus - 1]
    if index_bus < len(words) - 1 and words[index_bus + 1].isdigit():  # проверяем слово после автобуса
        return words[index_bus + 1]
    return None
