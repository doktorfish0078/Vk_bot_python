from random import randint
import re

def beautiful_num(num):
    if int(num) >= 0:
        new = ''
    else:
        new = '-'
        num=num[1:]
    for i in num:
        new += chr(ord(i) + 120744)
    return new


def roll(vk_session, id, min = 1, max = 100):
    if min > max:
        buf = min
        min = max
        max = buf
    result = str(randint(int(min), int(max)))
    return (
        "Случайное число  для @id{0}({1}) от {2} до {3} равняется {4}".format(
            id,
            vk_session.method('users.get', {'user_ids': id, 'name_case' : 'gen' })[0]['first_name'],
            min, max, beautiful_num(result)), result
    )

def diceroll(vk_session, id):
    result = str(randint(1, 6))
    return(
        '@id{0}({1}) бросает кубик 🎲 и получает число {2}{3}!'.format(
            id,
            vk_session.method('users.get', {'user_ids': id})[0]['first_name'],
            result, chr(ord(result) + 9807)
        ), result
    )

def flip(vk_session, id):
    result = ('решка' if randint(0, 1) == 1 else 'орел') if id != 146297737 else 'ребро ебать'
    return(
        '@id{0}({1}) бросает монетку, а выпадает ему {2}'.format(
            id,
            vk_session.method('users.get', {'user_ids': id})[0]['first_name'],
            result
        ), result
    )