from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import datetime
from PIL import Image
from io import BytesIO

def get_schedule_bus():
    now = datetime.datetime.now()
    URL = "https://igis.ru/gortrans/bus/izh/19"
    driver = webdriver.PhantomJS()
    driver.set_window_size(1600, 2070)
    driver.get(URL)
    elem = driver.find_element_by_class_name("table-st1")
    screen = driver.get_screenshot_as_png()
    rect = elem.rect  # {'height': 1041, 'width': 722, 'x': 562, 'y': 689}
    box = (rect['x'], rect['y'], rect['x'] + rect['width'], rect['y'] + rect['height'])
    im = Image.open(BytesIO(screen))
    print(im)
    region = im.crop(box) # вырезаем
    print(region)
    region.save("screenshots\screen_" + now.strftime("%d-%m-%Y %H-%M-%S") + ".png", 'PNG')
    driver.quit()
    print("Удачно")
get_schedule_bus()