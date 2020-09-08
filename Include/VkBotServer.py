# -*- coding: utf-8 -*-
# лох по кличке ортом id = 146297737

import random

from Commands import weather, schedule, skirmish, myanimelist,\
    how_week, schedule_bus, list_commands, diceroll, greet, thanks_react

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

"""
 Идея в том, что мы будем записывать ивенты для каждого отдельного пользователя 
 в словарь. По одной штуке на пользователся (последний)
 В словаре имеется структура {id: [время ласт запроса:int, [доп. данные, ивент]]}
 По сообщению "Спасибо" массив очищается для отдельного пользователя И для пользователя,
  вызывавшего ту-же предпоследнюю команду (до Спасибо) 
  Значения в events_of_users[sender_id][1][1]:
   "q" - вопрос
   "h" - приветствие
   "s" - перестрелка !!! Результат сохраняется в формате [победивший, проигравший] предыдущим элементом перед "s" !!!
   "w" - погода
   "a" - аниме
   "r" - /roll !!! Значение /roll сохраняется предыдущим элементом перед "r" !!!
   "d" - /diceroll !!! Значение /diceroll сохраняется предыдущим элементом перед "d" !!!
   "f" - /flip !!! Значение /flip сохраняется предыдущим элементом перед "f" !!!
   "rasp" - Расписание
  
"""

events_of_users = {}

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
    sender_id = event.message['from_id']


    if (sender_id not in events_of_users.keys()) or (time() - events_of_users[sender_id][0] > 300):
        events_of_users[sender_id] = [time(), [None, None]]


    if "help" in msg_text or "команды" in msg_text:
        send_msg_tochat(chat_id, list_commands.get_commands())

    if 'перестрелка' in msg_text and '|' in msg_text:

        result = skirmish.skirmish(vk_session, sender_id, int(msg_text.split('|')[0].split('[')[1][2:]))
        send_msg_tochat(chat_id, result[0])

        events_of_users[sender_id][0] = time()
        events_of_users[sender_id][1] = [result[1], 's']

    elif 'погода' in msg_text or 'погоду' in msg_text:

        events_of_users[sender_id][0] = time()

        if 'завтра' in msg_text:
            result = weather.weather(True)
            send_msg_tochat(chat_id, result[0])
            events_of_users[sender_id][1] = [result[1], 'w']

        else:
            result = weather.weather()
            send_msg_tochat(chat_id, result[0])
            events_of_users[sender_id][1] = [result[1], 'w']

    elif 'расписание' in msg_text:

        events_of_users[sender_id][0] = time()
        events_of_users[sender_id][1] = [None, 'rasp']

        send_photo_tochat(chat_id, attachment=schedule.schedule())

    elif 'неделя' in msg_text and 'какая' in msg_text:

        events_of_users[sender_id][0] = time()
        events_of_users[sender_id][1] = [None, 'q']

        send_msg_tochat(chat_id, how_week.how_week())

    #elif 'автобус' in msg_text or 'автобуса' in msg_text:
        #send_msg_tochat(chat_id, "Ищу где Ваш автобус,подождите немного...")
        #send_photo_tochat(chat_id, path_to_photo=schedule_bus.get_path_schedule_bus(msg_text))

    elif (('хуета' in msg_text) or ('хуита' in msg_text)) and ('я' not in msg_text):
        send_msg_tochat(chat_id, 'Сам ты хуита понял? М? М? М?')

    elif 'тыква' in msg_text:
        send_msg_tochat(chat_id, 'А может ты ква??????!! Не понял')

    elif ('привет' in msg_text or 'здравствуй' in msg_text) and ('сладкий' in msg_text or 'бот' in msg_text) and \
            ((time() - greeted[sender_id]) > 6000 if sender_id in greeted.keys() else True):

        events_of_users[sender_id][0] = time()
        greeted[sender_id] = time()

        hello = greet.ortom_hello() if sender_id == ortom_id else greet.hello()

        send_msg_tochat(chat_id,
                        hello.format(
                            vk_session.method('users.get', {'user_ids': sender_id})[0]['first_name'])
                        )
    elif 'аниме' in msg_text:
        send_msg_tochat(chat_id, myanimelist.get_top())

        events_of_users[sender_id][0] = time()
        events_of_users[sender_id][1] = [None, 'a']

    elif 'секс' in msg_text:
        send_msg_tochat(chat_id, 'Ты тоже секс')

    elif '/' in msg_text:

        if 'roll' in msg_text:
            result = diceroll.roll(vk_session, sender_id, msg_text)
            send_msg_tochat(chat_id, result[0])

            events_of_users[sender_id][0] = time()
            events_of_users[sender_id][1] = [result[1], 'r']

        elif 'dice' in msg_text:
            result = diceroll.diceroll(vk_session, sender_id)
            send_msg_tochat(chat_id, result[0])

            events_of_users[sender_id][0] = time()
            events_of_users[sender_id][1] = [result[1], 'd']

        elif 'flip' in msg_text:
            result = diceroll.flip(vk_session, sender_id)
            send_msg_tochat(chat_id, result[0])

            events_of_users[sender_id][0] = time()
            events_of_users[sender_id][1] = [result[1], 'f']

    elif 'спасибо' in msg_text:
        if events_of_users[sender_id][1][1]:
            send_msg_tochat(chat_id, thanks_react.react(vk_session, sender_id,
                                                    events_of_users[sender_id][1][1], events_of_users[sender_id][1][0]))
        else:
            send_msg_tochat(chat_id, "Не за что, {0}".format(
                'Дорогая' if vk_session.method('users.get', {'user_ids': sender_id, 'fields': 'sex'})[0]['sex'] == 1 else "Дорогой"))
        events_of_users[sender_id] = [time(), [None, None]]


def main():
    """
    Запуск бота,слушает сервер,при получении сообщения обрабатывает полученное input'ом и выдаёт ответ,если в сообщении была получена команда
    :return:
    """
    print("Бот приступил к работе")
    #queue_event = []
    for event in longpoll.listen(): # Слушаем сервер
        if event.type == VkBotEventType.MESSAGE_NEW:
            print("Получено сообщение")
            if event.from_chat: # Обработка сообщений из чата
                parse_msg(event)
            elif event.from_user:
                pass
                """ 
                    Эту шнягу, я сичтаю, нужно доработать потом отдельно
                    >Обработка личных сообщений
                """
                # send_msg_touser(event.message['from_id'], input(event.message['text']))

if __name__ == '__main__':
    main()


