from random import randint

def ortom_hello():
    ortom_hello_str = ['Скучал по твоей попе, {0}', 'Люблю твои хоум видео, {0}', 'Пасаси, {0}',
                       'Привет твоей маме, {0}', 'Попу надо мыть, {0}']
    return ortom_hello_str[randint(0, len(ortom_hello_str) - 1)]

def hello():
    hello_str = ['Приветик, {0}', 'Здравствуй, О {0}', 'Снова ты, {0}?',
                 'Уже вернулись, {0}?', 'Хо-хо, а я тебя не ждал, {0}'
                 '{0}, какая встреча!']
    return hello_str[randint(0, len(hello_str) - 1)]