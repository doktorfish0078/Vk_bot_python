from random import randint

def ortom_hello():
    ortom_hello_str = ['Скучал по твоей попе', 'Люблю твои хоум видео', 'Пасаси', 'Привет твоей маме', 'Привет']
    return ortom_hello_str[randint(0, len(ortom_hello_str) - 1)]

def hello():
    hello_str = ['Данил']
    return hello_str[randint(0, len(hello_str) - 1)]