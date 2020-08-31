import random
import requests
from vk_api import VkApi
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType


token = "ee5ee2a15eae712b0b63dd92847a7a06cc9e5e0b4014d430b7fdde83897d9cd9cea7978a0754aae391607"
group_id = "186084635"
weather_key = 'f8d86841539730fb1174d076209c76a7'

vk_session = VkApi(token = token)
longpoll = VkBotLongPoll(vk_session, group_id)
vk = vk_session.get_api()

weather_cond = {'Rain': 'дождик', 'Snow': 'снегопадик', 'Clouds': 'тучки', 'Clear': 'чистое небо'}


def parse_message_chat(event):
    msg_text = event.message['text'].lower()
    chat_id = event.chat_id
    if 'перестрелка' in msg_text and '|' in msg_text:
        write_msg_tochat(chat_id, skirmish(event.message['from_id'], msg_text.split('|')[0].split('[')[1]))
    elif 'погода' in msg_text or 'погоду' in msg_text:
        if 'завтра' in msg_text:
            write_msg_tochat(chat_id, weather_tomorrow())
        else:
            write_msg_tochat(chat_id, 'Погода сегодня:')
            write_msg_tochat(chat_id, weather_today())
    elif (('хуета' in msg_text) or ('хуита' in msg_text)) and ('я' not in msg_text):
        write_msg_tochat(chat_id, 'Сам ты хуита понял? М? М? М?')
    elif 'тыква' in msg_text:
        write_msg_tochat(chat_id, 'А может ты ква??????!! Не понял')

def parse_message_user(event):
    msg_text = event.message['text'].lower()
    user_id = event.message['from_id']
    if user_id == 378922227:
        write_msg_toman(user_id, 'clown')
    else:
        write_msg_toman(event.message['from_id'], 'Ля, а я так не умею')
    if user_id == 146297737:
        write_msg_toman(event.message['from_id'], "Иди нахуй, клоwн")


def write_msg_toman(user_id,message):
    vk_session.method('messages.send', {'user_id': user_id, 'message': message, 'random_id': random.randint(0, 2048)})

def write_msg_tochat(chat_id,message):
    vk_session.method('messages.send', {'chat_id': chat_id, 'message': message, 'random_id': random.randint(0, 2048)})


def skirmish(player1, player2):
    a = random.randint(0, 1)
    if player1 == player2:
        return 'Нельзя в себя стрелять, а то зароскомнадзоришься'
    elif player1 == 146297737:
        return  'Победителем вышел @{0}'.format(player2)
    elif player2 == 146297737:
        return 'Победителем вышел @{0}'.format(player1)
    elif a == 0:
        return 'Победителем вышел @{0}'.format(player1)
    else:
        return 'Победителем вышел @{0}'.format(player2)


def weather_today():
    out_weather = ''
    try:
        weather = requests.get(
            'http://api.openweathermap.org/data/2.5/forecast?id=524901&APPID=f8d86841539730fb1174d076209c76a7&q=Izhevsk,ru').json()['list']
        for i in range(0, 7):
            timetimetime = (i * 3) + 3
            out_weather += "{0}:00, {1}ºC, {2} \n".format(
                                                                    timetimetime if timetimetime > 10 else '0'+str(timetimetime),
                                                                    int(float(weather[i]['main']['temp'])-273.15),
                                                                    weather_cond[weather[i]['weather'][0]['main']])
        return out_weather
    except BaseException:
        return 'Погода недоступна в настоящее время!'

def weather_tomorrow():
    out_weather = ''
    try:
        weather = requests.get(
            'http://api.openweathermap.org/data/2.5/forecast?id=524901&APPID=f8d86841539730fb1174d076209c76a7&q=Izhevsk,ru').json()['list']
        for i in range(7, 14):
                timetimetime = ((i-7) * 3) + 3
                out_weather += "{0}:00, {1}ºC, {2} \n".format(
                                                                    timetimetime if timetimetime > 10 else '0'+str(timetimetime),
                                                                    int(float(weather[i]['main']['temp']) - 273.15),
                                                                    weather_cond[weather[i]['weather'][0]['main']])
        return out_weather
    except BaseException:
        return 'Погода недоступна в настоящее время!'


def main():
    print("On")

    for event in longpoll.listen():
        print(event.message)
        if event.type == VkBotEventType.MESSAGE_NEW and event.from_chat:
            parse_message_chat(event)
        elif event.type == VkBotEventType.MESSAGE_NEW and event.from_user:
            parse_message_user(event)

if __name__ == '__main__':
    main()
