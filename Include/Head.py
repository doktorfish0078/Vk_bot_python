# -*- coding: utf-8 -*-
from Commands import weather, schedule, skirmish, myanimelist, \
    how_week, list_commands, diceroll, greet, thanks_react, test_wiki

from vk_api import VkApi
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType

import parse_comands, send_msg
from common_finder import find_common

from sys import exit
from re import split
from time import time

# "ee5ee2a15eae712b0b63dd92847a7a06cc9e5e0b4014d430b7fdde83897d9cd9cea7978a0754aae391607"
# 186084635

token = 'ee5ee2a15eae712b0b63dd92847a7a06cc9e5e0b4014d430b7fdde83897d9cd9cea7978a0754aae391607'
group_id = '186084635'

gods = []
low_rank = []

users = {}

# with open('params.txt', 'r') as parameters:
#     pass


class User:

    def __init__(self, sender_id):
        self.greeted = 0
        self.id = sender_id
        self.last_use = None
        self.current_chat = None
        self.last_event = None
        self.last_result = None

    def under_parse_message(self, message):
        message.lower()

        if message[0] == '/':
            uncut = split(r"[\s/':;?,.<>()*&%$#!]+", message[1:])
            print(uncut)
            message = []
            for under_str in uncut:
                if under_str: message.append(under_str)
        else:
            return None

        if time() - self.greeted < 30:
            self.parse_no_slash(message)
        else:
            self.parse_slash(message)

    def parse_slash(self, message):
        request = message[0]
        answer = ''

        if request in ['help', 'команды', 'помощь']:
            answer = list_commands.get_commands()

        elif request in ['anime', 'аниме']:
            self.last_event = 'a'
            answer = myanimelist.get_top()
            """
                Пока оставил без входящих атрибутов, непонятно как работать должно просто))
            """

        elif request in ['weather', 'погода']:
            self.last_event = 'w'
            if 'завтра' or 'tomorrow' in message:
                answer, self.last_result = weather.weather(tomorrow = True)
            else:
                answer, self.last_result = weather.weather()

        elif request in ['неделя', 'week']:
            self.last_event = 'q'
            answer = how_week.how_week()

        elif request in ['schedule', 'расписание']:
            self.last_event = 'rasp'
            attachment = schedule.schedule()
            send_msg.send_photo_fromVK_tochat(vk_session, self.current_chat, attachment)

        elif request in ['dice', 'кубик']:
            self.last_event = 'd'
            answer, self.last_result = diceroll.diceroll(vk_session, self.id)

        elif request in ['flip', 'монетка', 'coin']:
            self.last_event = 'f'
            answer, self.last_result = diceroll.flip(vk_session, self.id)

        elif request in ['roll', 'ролл']:
            if len(message) > 3:
                answer, self.last_result = diceroll.roll(vk_session, self.id, message[1], message[2])
            else:
                answer, self.last_result = diceroll.roll(vk_session, self.id)

        elif request in ['вики', 'wiki', 'wikipedia']:
            if len(message) > 1:
                answer = test_wiki.wiki_searching(','.join(message[1:]))

        elif request in []:
            pass

        elif request in ['привет', "здравствуй", "хай", "hello", 'hi']:
            if "бот" in request or 'bot' in request:
                greet.hello(vk_session, self.id)
                self.greeted = time()



        if answer:
            self.last_use = time()
            send_msg.send_msg_tochat(vk_session, self.current_chat, answer)



    def parse_no_slash(self, message):
        pass


def main():
    global vk_session
    vk_session = VkApi(token=token)
    longpoll = VkBotLongPoll(vk_session, group_id, wait=10)

    # try:
    print('Start')
    for event in longpoll.listen():

        if event.type == VkBotEventType.MESSAGE_NEW and event.from_chat:

            sender = event.message['from_id']

            if event.message['from_id'] not in users.keys():
                users[sender] = User(sender)

            users[sender].current_chat = event.chat_id

            if event.message['attachments'] and event.message['attachments'][0]['type'] == 'audio_message':
                    pass

            elif event.message['text']:
                users[sender].under_parse_message(event.message['text'])
    # except BaseException as error:
    #     send_msg(vk_session, 1, error)
    # finally:
    #     exit()


if __name__ == '__main__':
    main()
