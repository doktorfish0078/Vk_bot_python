import random


def skirmish(vk_session, player1, player2, gm=False):
    if not gm:
        a = random.randint(0, 1)
    if player1 == player2:
        return ('Нельзя в себя стрелять, а то зароскомнадзоришься', (player1, player2))
    elif player1 == 146297737:
        return ('Победитель, палучаица, @id{0}({1})'.format(
            player2,
            vk_session.method('users.get', {'user_ids': player2})[0]['first_name']
        ), (player2, player1))
    elif player2 == 146297737:
        return ('Победитель, палучаица, @id{0}({1})'.format(
            player1,
            vk_session.method('users.get', {'user_ids': player1})[0]['first_name']
        ), (player1, player2))
    elif a == 0:
        return ('Победитель, палучаица, @id{0}({1})'.format(
            player1,
            vk_session.method('users.get', {'user_ids': player1})[0]['first_name']
        ), (player1, player2))
    else:
        return ('Победитель, палучаица, @id{0}({1})'.format(
            player2,
            vk_session.method('users.get', {'user_ids': player2})[0]['first_name']
        ), (player2, player1))