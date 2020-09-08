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


def roll(vk_session, id, text_msg):
    min = 1
    max = 100
    try:
        borders_buf = [border for border in
                       re.split(r'[ ,]', re.search(r' *[\-+]?\d+ *[, ]+ *[\-+]?\d+ *', text_msg).group()) if
                       border != '']
        borders = [int(border) for border in borders_buf]
        borders.sort()
        min, max = borders
    except (AttributeError, TypeError, ValueError):
        # print("/roll crashed or auto-bordered")
        pass
    result = str(randint(int(min), int(max)))
    return (
        "Случайное число  для @id{0}({1}) от {2} до {3} равняется {4}".format(
            id,
            vk_session.method('users.get', {'user_ids': id, 'name_case' : 'gen' })[0]['first_name'],
            min, max, beautiful_num(result)
    ), result
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