from random import choice


def choose(text):
    try:
        return choice(text.split(',')).strip()
    except BaseException:
        return "Не из чего виберать сучара блять "