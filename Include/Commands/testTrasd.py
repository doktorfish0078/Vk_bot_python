from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import datetime


def get_schedule_bus():
    now = datetime.datetime.now()
    URL = "https://igis.ru/gortrans/bus/izh/19"
    try:
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        driver = webdriver.Chrome(options=chrome_options)
        driver.set_window_size(1600, 2070)
        driver.get(URL)
        elem = driver.find_element_by_class_name("table-st1")
        elem.screenshot(
            "screenshots\screen_" + now.strftime("%d-%m-%Y %H-%M-%S") + ".png")
        driver.quit()
    except BaseException():
        print("Ошибка подключения")

get_schedule_bus()