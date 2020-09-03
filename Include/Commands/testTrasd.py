from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import datetime
from PIL import Image
from io import StringIO

def get_schedule_bus():
    now = datetime.datetime.now()
    URL = "https://igis.ru/gortrans/bus/izh/29"
    driver = webdriver.PhantomJS()
    #driver.set_window_size(1600, 2070)
    driver.get(URL)
    elem = driver.find_element_by_class_name("table-st1")
    driver.save_screenshot("screenshots\screen_" + now.strftime("%d-%m-%Y %H-%M-%S") + ".png")

    screen = driver.get_screenshot_as_png()

    print(elem.location)
    print(elem.size)
    box = (elem.location['x'], elem.location['y'], elem.size['height'], elem.size['width'])
    im = Image.open(StringIO(screen))
    region = im.crop(box)
    region.save("screenshots\screen_" + now.strftime("%d-%m-%Y %H-%M-%S") + ".png", 'JPEG', optimize=True, quality=95)
    #elem.screenshot("screenshots\screen_" + now.strftime("%d-%m-%Y %H-%M-%S") + ".png")
    #elem.screenshot(
        #"screenshots\screen_" + now.strftime("%d-%m-%Y %H-%M-%S") + ".png")
    #driver.save_screenshot("screenshots\screen_" + now.strftime("%d-%m-%Y %H-%M-%S") + ".png")
    driver.quit()
    print("Удачно")
get_schedule_bus()