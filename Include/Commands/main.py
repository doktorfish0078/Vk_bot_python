# -*- coding: utf-8 -*-
import weather, schedule, skirmish, myanimelist, \
    how_week, list_commands, diceroll, greet, thanks_react

from vk_api import VkApi
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType

import parse_comands, send_msg

from sys import exit
from re import split
from time import time

# "ee5ee2a15eae712b0b63dd92847a7a06cc9e5e0b4014d430b7fdde83897d9cd9cea7978a0754aae391607"
# 186084635

global vk_session

token = 'ee5ee2a15eae712b0b63dd92847a7a06cc9e5e0b4014d430b7fdde83897d9cd9cea7978a0754aae391607'
group_id = ''

gods = []
low_rank = []

users = {}

with open('params.txt', 'r') as parameters:
    pass


class Users:

    def __init__(self):
        self.greeted = 0
        self.id = 0
        self.last_use = None
        self.last_event = None
        self.last_result = None

    def under_parse_message(self, message):

        if message[0] == '/':
            message = split("{[, /\|]}.?:;^%$#№<>()_=*&'"+'"', message[1:])
            self.last_use = time()
        else:
            return None

        if time() - self.greeted < 30:
            self.parse_no_slash(message)
        else:
            self.parse_slash(message)

    def parse_slash(self, message):
        request = message[0]

        if request == 'help' or 'команды':
            answer = list_commands.get_commands()

        elif request == 'anime' or 'аниме':
            self.last_event = 'a'
            answer = myanimelist.get_top()
            """
                Пока оставил без входящих атрибутов, непонятно как работать должно просто))
            """

        elif request == 'weather' or 'погода':
            self.last_event = 'w'
            if 'завтра' or 'tomorrow' in message:
                answer, self.last_result = weather.weather(True)
            else:
                answer, self.last_result = weather.weather()

        # elif request == ''



    def parse_no_slash(self, message):
        pass



def main():
    vk_session = VkApi(token=token)
    longpoll = VkBotLongPoll(vk_session, group_id, wait=10)

    try:
        for event in longpoll.listen():

            if event.type == VkBotEventType.MESSAGE_NEW and event.from_chat:

                sender = event.message['from_id']

                if event.message['from_id'] not in users.keys():
                    users[sender] = Users

                if event.message['attachments'] and event.message['attachments'][0]['type'] == 'audio_message':
                        pass

                elif event.message['text']:
                    users[sender].parse_messange(event.message['text'].lower)
    except BaseException as error:
        send_msg(vk_session, 1, error)
    finally:
        exit()


if __name__ == '__main__':
    main()
