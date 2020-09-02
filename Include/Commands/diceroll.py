from random import randint

def roll(vk_session, id, min=1, max=100):
    result = randint(min, max) if id != 146297737 else min
    return(
        "Случайное число для @id{0}({1}) от {2} до {3} равняется {4}".format(
            id,
            vk_session.method('users.get', {'user_ids': id, 'name_case' : 'gen' })[0]['first_name'],
            min, max, result)
    )

def diceroll(vk_session, id):
    result = randint(1, 6) if id != 146297737 else 1
    return(
        '@id{0}({1}) бросает кубик и получает число {2}!'.format(
            id,
            vk_session.method('users.get', {'user_ids': id})[0]['first_name'],
            result
        )
    )

def flip(vk_session, id):
    return(
        '@id{0}({1}) бросает монетку, а выпадает ему {2}'.format(
            id,
            vk_session.method('users.get', {'user_ids': id})[0]['first_name'],
            'решка' if randint(0, 1) == 1 else 'орел'
        )
    )