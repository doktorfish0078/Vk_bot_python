from random import randint

#  И пусть солнце сияет над твоего головой, путник!
#  И пусть дождь не будет проблемой для тебя!


def react(vk_session, sender_id, last_q, last_result=None):
    global vk
    global id
    id = sender_id
    vk = vk_session
    reacts = {
        'r': roll_r,
        'd': dicer_r,
        'f': flip_r,
        'q': quest_r,
        'w': weather_r,
        'a': anime_r,
        's': skirm_r,
        'rasp': rasp_r
    }
    return reacts.get(last_q)(last_result)

def roll_r(result):
    return "Да пожалуйста, {0}. Надеюсь, число {1} тебя устроило".format(
        'Дорогая' if vk.method('users.get', {'user_ids': id, 'fields': 'sex'})[0]['sex'] == 1 else "Дорогой",
        result
    )

def dicer_r(result):
    if result == 1:
        ansv = "Минимальное число, но не обижайся! Можно кинуть еще много кубиков"
    elif 1 < result < 6:
        ansv = "Неплохое число, {0}, не маленькое, но и не большое".format(result)
    else:
        ansv = "Максимально возможный результат, но не обольщайся (я тебе подкрутил, но больше не буду ;) )"

    return "Кидал этот кубик для тебя, {0}! {1}".format(
        'Дорогая' if vk.method('users.get', {'user_ids': id, 'fields': 'sex'})[0]['sex'] == 1 else "Дорогой",
        ansv
    )

def flip_r(_):
    return "Я всего-то подкинул монетку, но Пожалуйста"

def quest_r(_):
    return "Всегда пожалуйста, {0}!".format(
        'Миледи' if vk.method('users.get', {'user_ids': id, 'fields': 'sex'})[0]['sex'] == 1 else "Милорд"
    )

def weather_r(type):
    weather_type = {
        "Пасмурно": "Пожалуйста, и пусть эти небольшие тучи не расстраивают тебя на твоем пути!",
        "Ясно": "Не благодари, и пускай солнце сияет над твоей головой, Путник!",
        "Облачно": "Для этого я здесь! И пускай эти маленькие облачка не смутят тебя!",
        "Облачно с прояснениями": "Не за что! Эти облака никогда не смогут затмить такое Солнце, как Ты!",
        "Небольшой дождь": "Пожалуйста, " + ("Дорогая!" if vk.method('users.get', {'user_ids': id, 'fields': 'sex'})[0]['sex'] == 1 else "Дорогой!") \
        + "И не дай этому дождю размыть твой острый взор!",
        "Дождь": "Не стоит благодарностей, Дорогуша! И не дай этому дождю встать рпеградой между Тобой и Твоей целью",
        "Малооблачно": "Тебе спасибо, " + ("Дорогая!" if vk.method('users.get', {'user_ids': id, 'fields': 'sex'})[0]['sex'] == 1 else "Дорогой!") \
        + "Ты же не дашь этим тучкам разрушить твой энтузиазм сегодня, не правда ли?"
    }
    return weather_type[type]


def anime_r(_):
    return "Да не за что! Удачного просмотра!"

def skirm_r(result):
    return "Тебе спасибо! {0}".format(
        "Не расстраивайся, что не получилось перестрелять {0}. Всегда можно попросить реванш!".format(
            vk.method('users.get', {'user_ids': result[0], 'name_case': 'gen'})[0]['first_name']
        ) if result[0] != id else "Поздравляю с одержанной победой над {0}! Но опасайся расправы ;)".format(
            vk.method('users.get', {'user_ids': result[1], 'name_case': 'gen'})[0]['first_name']
        )
    )

def rasp_r(_):
    return "Всегда пожалуйста, и не опаздай на пару!"
