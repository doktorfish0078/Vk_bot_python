def punish(vk_session, to_punish):
    try:
        enemy_id = to_punish
    except BaseException:
        pass
    return 'Пососи, {0} @id{1}({2})'.format(
        ("собакоподобная пакость, не становись ортомом," if
         vk_session.method('users.get', {'user_ids': enemy_id, 'fields': 'sex'})[0]['sex'] == 1
         else "попущенный под столиком, грязный пасынок собаки"), enemy_id,
        vk_session.method('users.get', {'user_ids': enemy_id})[0]['first_name'])
