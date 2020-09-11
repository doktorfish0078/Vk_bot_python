from random import randint

smiles = [':>', 'O-o', '()∪()', '❪❫❣❪❫', ':-)', '⊙⊔⊙', '⊝o⊝', '∘∨∘', ':3', '*@*']

def ortom_hello():
    ortom_hello_str = ['Скучал по твоей попке, {0} ', 'Люблю твои хоум видео, {0} ', 'Пасаси, {0} ',
                       'Привет твоей маме, {0} ', 'Попку надо мыть, {0} ',
                       'Сука, опять ты, {0}? Мляяяяя']
    return ortom_hello_str[randint(0, len(ortom_hello_str) - 1)]

def hello(vk_session, id):
    hello_str = ['Приветик, {0} ', 'Здравствуй, {0} ', 'Снова ты, {0}? ',
                 'Уже вернулись, {0}? ', 'Хо-хо, а я тебя не ждал, {0} ',
                 '{0}, какая встреча! ']
    return hello_str[randint(0, len(hello_str) -1)] + smiles[randint(0, len(hello_str) -1)].format(
        vk_session.method('users.get', {'user_ids': id})[0]['first_name']
    )
