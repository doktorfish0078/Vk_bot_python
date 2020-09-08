import random


def skirmish(vk_session, player1, player2):
    a = random.randint(0, 1)
    if player1 == player2:
        return 'Нельзя в себя стрелять, а то зароскомнадзоришься'
    elif player1 == 146297737:
        return 'Победитель, палучаица, @id{0}({1})'.format(
            player2,
            vk_session.method('users.get', {'user_ids': player2})[0]['first_name']
        )
    elif player2 == 146297737:
        return 'Победитель, палучаица, @id{0}({1})'.format(
            player1,
            vk_session.method('users.get', {'user_ids': player1})[0]['first_name']
        )
    elif a == 0:
        return 'Победитель, палучаица, @id{0}({1})'.format(
            player1,
            vk_session.method('users.get', {'user_ids': player1})[0]['first_name']
        )
    else:
        return 'Победитель, палучаица, @id{0}({1})'.format(
            player2,
            vk_session.method('users.get', {'user_ids': player2})[0]['first_name']
        )