import random

import requests
from selenium import webdriver
import datetime
from PIL import Image
from io import BytesIO

from vk_api import VkApi, VkUpload
from vk_api.bot_longpoll import VkBotLongPoll

token = "ee5ee2a15eae712b0b63dd92847a7a06cc9e5e0b4014d430b7fdde83897d9cd9cea7978a0754aae391607"
group_id = "186084635"


ortom_id = 146297737

# Для Long Poll
vk_session = VkApi(token=token)

# Для использоания Long Poll API
#longpoll = VkBotLongPoll(vk_session, group_id, wait=10)

# Для загрузки фото и других мультимедиа в сообщения
upload = VkUpload(vk_session)

vk_api = vk_session.get_api()


def get_schedule_bus():
    now = datetime.datetime.now()
    URL = "https://igis.ru/gortrans/bus/izh/29"
    driver = webdriver.PhantomJS()
    driver.set_window_size(1600, 2070)
    driver.get(URL)
    elem = driver.find_element_by_class_name("table-st1")
    screen = driver.get_screenshot_as_png()
    rect = elem.rect  # {'height': 1041, 'width': 722, 'x': 562, 'y': 689}
    box = (rect['x'], rect['y'], rect['x'] + rect['width'], rect['y'] + rect['height'])
    print(screen)
    im = Image.open(BytesIO(screen))
    region = im.crop(box) # вырезаем
    return region.tobytes()
    #region.save("screenshots\screen_" + now.strftime("%d-%m-%Y %H-%M-%S") + ".png", 'PNG')
    #driver.quit()
    print("Удачно")


get_schedule_bus()
url = requests.get('https://i1.wp.com/www.joshsfrogs.com/catalog/blog/wp-content/uploads/2013/01/ball-python.jpg').content
#print(url)
image_data = get_schedule_bus()
upload_url = vk_api.photos.getMessagesUploadServer(group_id=group_id)['upload_url']
image_name = "kek{}.png".format(random.randint(0, 10))
r = requests.post(upload_url, files={'photo': (image_name, image_data) }).json()
d = {}
d['server'] = r['server']
d['photo'] = r['photo']
d['hash'] = r['hash']
d['group_id'] = group_id

photo = vk_api.photos.saveMessagesPhoto(**d)[0]

attachment = "photo{}_{}_{}".format(photo['owner_id'], photo['id'], photo['access_key'])
vk_session.method("messages.send",
                    {"chat_id": 2, "message": "", "attachment": attachment, "random_id": random.randint(0, 2048)})
