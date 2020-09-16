# -*- coding: utf-8 -*-
from Commands import weather, schedule, skirmish, myanimelist, \
    how_week, list_commands, diceroll, greet, thanks_react, special, \
    test_films, schedule_bus

    # test_wiki, \

from vk_api import VkApi
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType

import parse_comands, send_msg
import post_request_to_VK
from common_finder import find_common
from sys import path
from random import randint

from sys import exit
from re import split
from time import time

token = '3390b47bcb8faa9ba278d163df8c7b8b456275c52931cffaf4d1993733575f379e2d3fc56a38db8ef7624'
group_id = '198707501'

gods = []
banned = {}
try:
    with open(path[0] + '/params.txt', 'r') as god:
        params = god.readlines()

        for god in params:
            gods.append(int(god.split('\n')[0]))

except FileNotFoundError:
    print('Не найдены боги!')

#нужно сделать числами!
users = {}


class User:

    def __init__(self, sender_id):
        self.greeted = 0
        self.slash_needed = True
        self.id = sender_id
        self.last_use = None

        self.copied_text = ''

        self.current_chat = None #chat_id

        self.last_event = None
        self.last_result = None

    def under_parse_message(self, msg):
        message = msg['text'].lower()
        is_command = False

        if message == '/':
            message += 'slash '

        if message == '/?':
            message += 'status'

        if message[0] == '/' or not self.slash_needed:
            is_command = True
            # uncut = split(r"[\s/':;?,.<>()*&%$#!]+", message)
            # новый вариант, старое удалим после успешного стресс-теста:
            uncut = split(r"[^\-\w]+", message)
            message = [word for word in uncut if len(word) > 0]
            # почему генераторы не юзаем?
            # for under_str in uncut:
            #     if under_str:
            #         message.append(under_str)
            if len(message) == 0:
                return None
        else:
            return None

        print(message)

        if is_command:
            self.parse(message, msg)

    def parse(self, words_from_msg, msg):
        request = words_from_msg[0]
        answer = ''

        # try:
        if request in ['help', 'команды', 'помощь']:
            answer = list_commands.get_commands()

        elif request in ['anime', 'аниме']:
            self.last_event = 'a'
            answer = myanimelist.get_top()
            """
                Пока оставил без входящих атрибутов, непонятно как работать должно просто))
            """

        elif request in ['cinema', 'film', 'films', 'кино']:
            answer = test_films.get_films()

        elif request in ['weather', 'погода']:
            self.last_event = 'w'
            if 'завтра' in words_from_msg or 'tomorrow' in words_from_msg:
                answer, self.last_result = weather.weather(tomorrow = True)
            else:
                answer, self.last_result = weather.weather()

        elif request in ['неделя', 'week']:
            self.last_event = 'q'
            answer = how_week.how_week()

        elif request in ['schedule', 'расписание']:
            self.last_event = 'rasp'
            attachment = schedule.schedule(self.current_chat)
            send_msg.send_photo_fromVK_tochat(vk_session, self.current_chat, attachment)

        elif request in ['dice', 'кубик', '🎲']:
            self.last_event = 'd'
            answer, self.last_result = diceroll.diceroll(vk_session, self.id)

        elif request in ['flip', 'монетка', 'coin']:
            self.last_event = 'f'
            answer, self.last_result = diceroll.flip(vk_session, self.id)

        elif request in ['roll', 'ролл']:
            try:
                answer, self.last_result = diceroll.roll(vk_session, self.id, int(words_from_msg[1]), int(words_from_msg[2]))
            except BaseException:
                answer, self.last_result = diceroll.roll(vk_session, self.id,)

        # elif request in ['вики', 'wiki', 'wikipedia']:
        #     if len(message) > 1:
        #         answer = test_wiki.wiki_searching(','.join(message[1:]))

        # elif request in ['автобус', 'автобуса']:
        #     send_msg.send_msg_tochat(vk_session, self.current_chat,
        #                              'Получаем расписание вашего автобуса... Ожидайте около 10-15 секунд,'
        #                              'в зависимости от лагов в ВК ;)')
        #     attachment = post_request_to_VK.get_attachment(
        #         vk_api, schedule_bus.get_byte_screen_schedule_bus(' '.join(words_from_msg)))
        #     if attachment:
        #         self.last_event = 'bus'
        #         send_msg.send_photo_fromVK_tochat(vk_session, self.current_chat,attachment)
        #     else:
        #         answer = 'Не удалось получить расписание автобуса :('


        elif request in ['привет', "здравствуй", "хай", "hello", 'hi'] and time() - self.greeted > 600:
            if "бот" in request or 'bot' in request:
                greet.hello(vk_session, self.id)
                self.greeted = time()

        elif request in ['save', 'скопировать', 'copy']:
            msg['text'] += ' '
            self.copied_text = msg['text'].split(' ', 1)[1]

        elif request in ['paste', 'вставить', 'print']:
            answer = self.copied_text

        elif request in ['skirmish', 'перестрелка', "🔫", 'bang', 'маслина']:
            if len(words_from_msg) >= 2:
                try:
                    second_warrior = int(words_from_msg[1].split('|')[0][3:])
                    answer, self.last_result = skirmish.skirmish(vk_session, self.id, second_warrior)
                except BaseException:
                    answer = ''
            else:
                answer = 'А по кому стрелять то? По воробьям? Победили воробьи'

        elif request in ['slash']:
            self.slash_needed = not self.slash_needed
            answer = 'Slash: {0}'.format('on' if self.slash_needed else 'off')

        elif request in ['status']:
            answer = 'Slash needed: {0}'.format('Yes' if self.slash_needed else 'No')

        elif request in ['punish', 'наказать', "наказание"]:
            if len(words_from_msg) > 1:
                try:
                    answer = special.punish(vk_session, self.id in gods, words_from_msg[1].split('|')[0][3:])
                except BaseException:
                    pass



        if answer:
            self.last_use = time()
            send_msg.send_msg_tochat(vk_session, self.current_chat, answer)
        #
        # except BaseException as error:
        #     send_msg.send_msg_tochat(vk_session, 1, 'An Error occurred! {}'.format(error))
        #

def main():
    global vk_session
    global vk_api
    vk_session = VkApi(token=token)
    longpoll = VkBotLongPoll(vk_session, group_id, wait=10)
    vk_api = vk_session.get_api()
    # try:
    print('Start')
    for event in longpoll.listen():
        if event.type == VkBotEventType.MESSAGE_NEW and event.from_chat:
            sender = event.message['from_id']

            if sender not in users.keys():
                users[sender] = User(sender)

            users[sender].current_chat = event.chat_id

            if event.message['attachments'] and event.message['attachments'][0]['type'] == 'audio_message':
                    pass

            elif event.message['text']:
                users[sender].under_parse_message(event.message)

    # except BaseException as error:
    #     send_msg(vk_session, 1, error)
    # finally:
    #     exit()


if __name__ == '__main__':
    main()
