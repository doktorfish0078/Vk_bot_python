from random import randint
import re

def beautiful_num(num):
    new = '' if int(num)>=0 else '-'
    for i in num[1:]:
        new += chr(ord(i) + 120744)
    return new


def roll(vk_session, id, text_msg):
    min = 1
    max = 100
    try:
        borders = re.search(r'\(\s*[\-+]?\d+\s*,\s*[\-+]?\d+\s*\)', text_msg).group()[1:-1].split(',')
        if int(borders[0]) > int(borders[1]):
            borders.reverse()
        print(borders)
        min, max = borders
    except (AttributeError, TypeError):
        pass
    result = str(randint(int(min), int(max)))
    return(
        "Случайное число  для @id{0}({1}) от {2} до {3} равняется {4}".format(
            id,
            vk_session.method('users.get', {'user_ids': id, 'name_case' : 'gen' })[0]['first_name'],
            min, max, beautiful_num(result)
    )
    )

def diceroll(vk_session, id):
    result = str(randint(1, 6))
    return(
        '@id{0}({1}) бросает кубик 🎲 и получает число {2}{3}!'.format(
            id,
            vk_session.method('users.get', {'user_ids': id})[0]['first_name'],
            result, chr(ord(result) + 9807)
        )
    )

def flip(vk_session, id):
    return(
        '@id{0}({1}) бросает монетку, а выпадает ему {2}'.format(
            id,
            vk_session.method('users.get', {'user_ids': id})[0]['first_name'],
            ('решка' if randint(0, 1) == 1 else 'орел') if id != 146297737 else 'ребро ебать'
        )
    )