from random import randint


def punish(vk_session, to_punish):
    try:
        enemy_id = to_punish
    except BaseException:
        pass
    sex = vk_session.method('users.get', {'user_ids': enemy_id, 'fields': 'sex'})[0]['sex']
    first_name = vk_session.method('users.get', {'user_ids': enemy_id})[0]['first_name']

    punishment_options_man = {
        0: 'Пососи, попущенный под столиком грязный пасынок собаки @id{}({})'.format(enemy_id, first_name),
        1: 'Ты -- тупая сука, @id{}({}), мои sicario будут трахать тебя перед тем как вырезать все твои органы, '
           'чтобы просто съесть их'.format(enemy_id, first_name),
        2: 'Черный воронок едет за вами, @id{}({}) 🚗🚗🚗 Готовься к лагерю, а точнее, к месту у параши'.format(
            enemy_id,
            first_name),
        3: 'Однажды меня спросили: "@id{}({}) сосёт?".\nЯ не ответил, ведь, как оказалось, это был не вопрос'.format(
            enemy_id, first_name),
        4: 'Ты думаешь это шутка? Нет, @id{}({}), шутка это твоя жизнь блять, при этом не очень удачная'.format(
            enemy_id, first_name),
        5: 'Я ебал жену @id{}({})!\nМне сасала дочь @id{}({})!\nКак тебе рифма?'.format(enemy_id,
                            vk_session.method('users.get', {'user_ids': enemy_id, 'name_case':'gen'})[0]['first_name'],
                                                                                      enemy_id,
                            vk_session.method('users.get', {'user_ids': enemy_id, 'name_case':'gen'})[0]['first_name'])
    }

    punishment_options_woman = {
        0: 'Пососи, собакоподобная пакость, не становись ортомом, @id{}({})'.format(enemy_id, first_name),
        1: 'Женщина -- лучший друг человека, но ты, @id{}({}), явно лучший друг ортёма (фу)'.format(enemy_id, first_name),
        2: 'Пажилая сперма капает на твоё личико, @id{}({}), подобное поведение явно стало твоей ошибкой'.format(
            enemy_id, first_name),
        3: 'Кто волки, кто овцы... А ты, @id{}({}) -- просто конченная овца'.format(enemy_id, first_name)
    }

    rand = randint(0, len(punishment_options_man) - 1) if sex == 2 else randint(0, len(punishment_options_woman) - 1)
    return punishment_options_man[rand] if sex == 2 else punishment_options_woman[rand]
