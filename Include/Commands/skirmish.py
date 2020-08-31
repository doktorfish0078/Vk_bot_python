import random


def skirmish(player1, player2):
    a = random.randint(0, 1)
    if player1 == player2:
        return 'Нельзя в себя стрелять, а то зароскомнадзоришься'
    elif player1 == 146297737:
        return  'Победителем вышел @{0}'.format(player2)
    elif player2 == 146297737:
        return 'Победителем вышел @{0}'.format(player1)
    elif a == 0:
        return 'Победителем вышел @{0}'.format(player1)
    else:
        return 'Победителем вышел @{0}'.format(player2)