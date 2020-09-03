from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import datetime


def get_schedule_bus():
    now = datetime.datetime.now()
    URL = "https://igis.ru/gortrans/bus/izh/29"
    driver = webdriver.
    #driver.set_window_size(1600, 2070)
    driver.get(URL)
    elem = driver.find_element_by_class_name("table-st1")
    print(elem)
    #elem.screenshot("screenshots\screen_" + now.strftime("%d-%m-%Y %H-%M-%S") + ".png")
    #elem.screenshot(
        #"screenshots\screen_" + now.strftime("%d-%m-%Y %H-%M-%S") + ".png")
    #driver.save_screenshot("screenshots\screen_" + now.strftime("%d-%m-%Y %H-%M-%S") + ".png")
    driver.quit()
    print("Удачно")
get_schedule_bus()