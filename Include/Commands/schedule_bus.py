from selenium import webdriver
from PIL import Image
from io import BytesIO
from sys import path

import re


def get_byte_screen_schedule_bus(text_msg):
    """
    :param text_msg:
    :return: Возвращает бинарный вид png скриншота
    """

    URL = "https://igis.ru/gortrans/bus/izh/"  # izh/номер автобуса
    numb_bus = get_numb_bus(text_msg)
    if numb_bus is None or not(2 <= int(numb_bus) <= 400):
        print('Не был распознан номер автобуса или нет автобуса с таким номером')
        return None
    URL += numb_bus
    print(path[0] + '\phantomjs')
    driver = webdriver.PhantomJS(path[0] + '/phantomjs')
    driver.set_window_size(1600, 2070)
    try:
        driver.get(URL)
        elem = driver.find_element_by_class_name("table-st1")  # находим нужный нам элемент
        screen = driver.get_screenshot_as_png()  # получаем байтовое представление скриншота
        rect = elem.rect  # {'height': 1041, 'width': 722, 'x': 562, 'y': 689} получаем расположение нужного элемента
        box = (
            rect['x'], rect['y'], rect['x'] + rect['width'],
            rect['y'] + rect['height'])  # делаем коробку для обреза фото
        im = Image.open(BytesIO(screen))  # открывает скрин
        region = im.crop(box)  # вырезаем
        b = BytesIO()
        region.save(b, 'png')
        driver.quit()
        return b.getvalue()
    except BaseException:
        print("Ошибка получения скриншота с адреса " + URL)
        return "None"


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

get_byte_screen_schedule_bus('автобус 19')