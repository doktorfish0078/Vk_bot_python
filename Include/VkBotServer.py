# -*- coding: utf-8 -*-
# лох по кличке ортом id = 146297737

import random

from Commands import weather, schedule, skirmish, myanimelist,\
    how_week, schedule_bus, list_commands, diceroll, greet

from vk_api import VkApi, VkUpload
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType

from time import time

token = "ee5ee2a15eae712b0b63dd92847a7a06cc9e5e0b4014d430b7fdde83897d9cd9cea7978a0754aae391607"
group_id = "186084635"


ortom_id = 146297737

# Для Long Poll
vk_session = VkApi(token=token)

# Для использоания Long Poll API
longpoll = VkBotLongPoll(vk_session, group_id, wait=30)

# Для загрузки фото и других мультимедиа в сообщения
upload = VkUpload(vk_session)

# Для вызова методов vk_api
#vk_api = vk_session.get_api()

greeted = {}

def send_msg_tochat(chat_id, message):
    """
    Отправка сообщения через метод messages.send
    :param chat_id: id чата, который получит сообщение
    :param message: содержимое отправляемого письма
    :return: None
    """
    vk_session.method('messages.send',
                      {'chat_id': chat_id, 'message': message, 'random_id': random.randint(0, 2048)})


def send_msg_touser(user_id, message):
    """
    Отправка сообщения через метод messages.send
    :param chat_id: id чата, который получит сообщение
    :param message: содержимое отправляемого письма
    :return: None
    """
    vk_session.method('messages.send',
                           {'user_id': user_id, 'message': message, 'random_id': random.randint(0, 2048)})


def send_photo_fromVK_tochat(chat_id, attachment):
    """
    :param chat_id:
    :param attachment:  вида photo-57846937_457307562,string
    :return:
    """
    vk_session.method("messages.send",
              {"chat_id": chat_id, "message": "", "attachment": attachment, "random_id": random.randint(0, 2048)})


def send_photo_tochat(chat_id, path_to_photo=None, attachment=None):
    """

    :param chat_id: id чата(беседы)
    :param path_to_photo: путь к фото на пк
    :param attachment: медиавложения к личному сообщению, перечисленные через запятую. Каждое прикрепление представлено в формате:
    <type><owner_id>_<media_id>
    В случае, если прикрепляется объект, принадлежащий другому пользователю добавлять к вложению его access_key в формате
    <type><owner_id>_<media_id>_<access_key>
    :return:
    """
    if path_to_photo:
        photo = upload.photo_messages(path_to_photo)
        attachment = "photo" + (str)(photo[0]['owner_id']) + "_" + (str)(photo[0]['id']) + "_" + (str)(photo[0]['access_key'])
    vk_session.method("messages.send",
                    {"chat_id": chat_id, "message": "", "attachment": attachment, "random_id": random.randint(0, 2048)})


def parse_msg(event):
    msg_text = event.message['text'].lower()
    chat_id = event.chat_id

    if "help" in msg_text or "команды" in msg_text:
        send_msg_tochat(chat_id,list_commands.get_commands())

    if 'перестрелка' in msg_text and '|' in msg_text:
        send_msg_tochat(chat_id, skirmish.skirmish(vk_session, event.message['from_id'], int(msg_text.split('|')[0].split('[')[1][2:])))

    elif 'погода' in msg_text or 'погоду' in msg_text:
        if 'завтра' in msg_text:
            send_msg_tochat(chat_id, weather.weather_tm())
        else:
            send_msg_tochat(chat_id, weather.weather_td())

    elif 'расписание' in msg_text:
        send_photo_tochat(chat_id, attachment=schedule.schedule())

    elif 'неделя' in msg_text and 'какая' in msg_text:
        send_msg_tochat(chat_id, how_week.how_week())

    #elif 'автобус' in msg_text or 'автобуса' in msg_text:
        #send_msg_tochat(chat_id, "Ищу где Ваш автобус,подождите немного...")
        #send_photo_tochat(chat_id, path_to_photo=schedule_bus.get_path_schedule_bus(msg_text))

    elif (('хуета' in msg_text) or ('хуита' in msg_text)) and ('я' not in msg_text):
        send_msg_tochat(chat_id, 'Сам ты хуита понял? М? М? М?')
    elif 'тыква' in msg_text:
        send_msg_tochat(chat_id, 'А может ты ква??????!! Не понял')
    elif 'спасибо' in msg_text:
        send_msg_tochat(chat_id, 'Если чем-то помог, то пожалуйста:3' if random.randint(1, 5) > 1 else 'Иди нахуй')
    elif ('привет' in msg_text or 'здравствуй' in msg_text) and ('сладкий' in msg_text or 'бот' in msg_text) and (greeted[event.message['from_id']] > 600):
        greeted[event.message['from_id']] = time()
        if event.message['from_id'] == ortom_id:
            hello = greet.ortom_hello()
        else:
            greet.hello()
        send_msg_tochat(chat_id, hello.format(
            vk_session.method('users.get', {'user_ids': event.message['from_id']})[0]['first_name']))
    elif 'сладкий' in msg_text or 'бот' in msg_text:
        send_msg_tochat(chat_id, 'Звали?')
    elif 'аниме' in msg_text:
        send_msg_tochat(chat_id, myanimelist.get_top())
    elif 'секс' in msg_text:
        send_msg_tochat(chat_id, 'Ты тоже секс')
    elif '/' in msg_text:
        if 'roll' in msg_text:
            send_msg_tochat(chat_id, diceroll.roll(vk_session, event.message['from_id'], msg_text))
        elif 'dice' in msg_text:
            send_msg_tochat(chat_id, diceroll.diceroll(vk_session, event.message['from_id']))
        elif 'flip' in msg_text:
            send_msg_tochat(chat_id, diceroll.flip(vk_session, event.message['from_id']))


def record_queue_event(queue_event,add_event,len_queue):
    """
    :param queue_event: очередь, в которую добавляются event'ы
    :param add_event: добавляемый event
    :param len_queue: длина желаемой очереди, например 10. В таком случая если в очереди уже есть 10 элементов,то самый последний удалиться,тем самым освободив место
    :return:
    """
    if len(queue_event) == len_queue:
        del queue_event[0]
    queue_event.append(add_event)


def main():
    """
    Запуск бота,слушает сервер,при получении сообщения обрабатывает полученное input'ом и выдаёт ответ,если в сообщении была получена команда
    :return:
    """
    print("Бот приступил к работе")
    #queue_event = []
    for event in longpoll.listen(): # Слушаем сервер
        for key in greeted.keys():
            greeted[key] += time() - greeted[key]
        if event.type == VkBotEventType.MESSAGE_NEW:
            print("Получено сообщение")
            #record_queue_event(queue_event,event,len_queue=3)
            if event.from_chat: # Обработка сообщений из чата
                parse_msg(event)
            elif event.from_user:
                send_msg_touser(event.message['from_id'], input(event.message['text']))
        # Обработка личных сообщений сообщества

if __name__ == '__main__':
    main()


