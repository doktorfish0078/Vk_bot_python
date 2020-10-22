# -*- coding: utf-8 -*-
from Commands import weather, schedule, skirmish, myanimelist, \
    how_week, list_commands, diceroll, greet, thanks_react, special, \
    test_films, choose \
    # , schedule_bus

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

global users
users = {}


class User:

    def __init__(self, sender_id):
        self.greeted = 0
        self.slash_needed = True
        self.id = sender_id
        self.last_use = None
        self.name = vk_session.method('users.get', {'user_ids': sender_id})[0]['first_name']

        self.copied_text = ''

        self.current_chat = None #chat_id

        self.last_event = None
        self.last_result = None

        self.banned = time()
        self.banned_for = 0

    def under_parse_message(self, msg):
        message = msg['text'].lower()
        is_command = False

        if message == '/':
            message += 'slash '

        if message == '/?':
            message += 'status'

        if message[0] == '/' or not self.slash_needed:
            is_command = True
            uncut = split(r"[^\-\w]+", message)
            message = [word for word in uncut if len(word) > 0]

            if len(message) == 0:
                return None
        else:
            return None

        print(message)

        if is_command:
            if (self.banned + self.banned_for <= time()):
                self.parse(message, msg)

    def parse(self, words_from_msg, msg):
        request = words_from_msg[0]
        answer = ''
        #
        try:
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
                        second_warrior = int(words_from_msg[1].split('|')[0][2:])
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
                        answer = special.punish(vk_session, self.id in gods, words_from_msg[1][2:], self.id)
                    except BaseException:
                        pass

            if request in ['idea', 'идея', 'передложение']:
                if self.id != 146297737:
                    for user in gods:
                        try:
                            send_msg.send_msg_touser(vk_session, user, '@id{}(new_idea): '.format(self.id)+msg['text'].lower().split(request)[1])
                        except BaseException:
                            pass

            if request in ['choose', 'выбрать', 'выбери']:
                answer = choose.choose(msg['text'].lower().split(request))

            if request in ['break_bot']:
                if self.id in gods:
                    exit()

            if request in ['ban', 'бан', "blacklist"]:
                if self.id in gods:
                    try:
                        to_ban = int(words_from_msg[1][2:])
                        if to_ban in users.keys():
                            to_ban_user = users[to_ban]
                        else:
                            users[to_ban] = User(to_ban)
                            to_ban_user = users[to_ban]

                        to_ban_user.banned = time()
                        if len(words_from_msg) > 3:
                            to_ban_user.banned_for = int(words_from_msg[3]) * 60
                        else:
                            to_ban_user.banned_for = 60
                        answer = "Пользователь @id{} не может пользоваться ботом".format(to_ban)

                    except (IndexError, TypeError) as error:
                        answer = 'А каво банить та а каво каво'
                        print(error)

                else:
                    self.banned = time()
                    self.banned_for = 300
                    answer = '@id{}({}) попытался кого-то забанить, но забанился сам на 5 минут'.format(self.id, self.name)

            if answer:
                self.last_use = time()
                send_msg.send_msg_tochat(vk_session, self.current_chat, answer)

        except BaseException as error:
            send_msg.send_msg_tochat(vk_session, 1, 'An Error occurred! {}'.format(error))


def main():
    global vk_session
    global vk_api
    vk_session = VkApi(token=token)
    longpoll = VkBotLongPoll(vk_session, group_id, wait=10)
    vk_api = vk_session.get_api()
    try:
        while True:
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

    except BaseException as error:
        print(error)



if __name__ == '__main__':
    main()
