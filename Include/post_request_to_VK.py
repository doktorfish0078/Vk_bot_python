import requests

from random import randint


def get_attachment(vk_api, multi_form_data_image):
    """
    :param vk_api: vk_api = vk_session.get_api() дл использования методов вк апи
    :param multi_form_data_image: бинарник фотографии ByteIO, можно получить c помощью requests.get(url).content
    :return: attachment вида <type><owner_id>_<media_id>_<access_key>
    """
    image_data = multi_form_data_image
    try:
        upload_url = vk_api.photos.getMessagesUploadServer()[
            'upload_url']  # получаем url от вк куда можно будет залить фото
        image_name = "kek{}.png".format(randint(0, 10))  # делаем рандомное имя фотки
        r = requests.post(upload_url, files={'photo': (image_name, image_data)}).json()  # посылаем пост запрос вк

        d = {}
        d['server'] = r['server']
        d['photo'] = r['photo']
        d['hash'] = r['hash']

        photo = vk_api.photos.saveMessagesPhoto(**d)[0]  # сохраняем на их сервере,как гласит документация

        return "photo{}_{}_{}".format(photo['owner_id'], photo['id'], photo['access_key'])
    except BaseException:
        print('Ошибка получения attachment при Post-запросе к вк')
        return None
