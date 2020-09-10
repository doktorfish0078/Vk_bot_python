from random import randint
from vk_api import VkUpload


def send_msg_tochat(vk_session, chat_id, message):
    """
    Отправка сообщения через метод messages.send
    :param chat_id: id чата, который получит сообщение
    :param message: содержимое отправляемого письма
    :return: None
    """
    vk_session.method('messages.send',
                      {'chat_id': chat_id, 'message': message, 'random_id': randint(0, 2048)})\


def send_msg_touser(vk_session, user_id, message):
    """
    Отправка сообщения через метод messages.send
    :param chat_id: id чата, который получит сообщение
    :param message: содержимое отправляемого письма
    :return: None
    """
    vk_session.method('messages.send',
                      {'user_id': user_id, 'message': message, 'random_id': randint(0, 2048)})


def send_photo_fromVK_tochat(vk_session, chat_id, attachment):
    """
    :param chat_id:
    :param attachment:  вида photo-57846937_457307562,string
    :return:
    """
    vk_session.method("messages.send",
                      {"chat_id": chat_id, "message": "", "attachment": attachment,
                       "random_id": randint(0, 2048)})


def send_photo_tochat(vk_session, chat_id, path_to_photo=None, attachment=None):
    """

    :param chat_id: id чата(беседы)
    :param path_to_photo: путь к фото на пк
    :param attachment: медиавложения к личному сообщению, перечисленные через запятую. Каждое прикрепление представлено в формате:
    <type><owner_id>_<media_id>
    В случае, если прикрепляется объект, принадлежащий другому пользователю добавлять к вложению его access_key в формате
    <type><owner_id>_<media_id>_<access_key>
    :return:
    """
    upload = VkUpload(vk_session)

    if path_to_photo:
        photo = upload.photo_messages(path_to_photo)
        attachment = "photo" + (str)(photo[0]['owner_id']) + "_" + (str)(photo[0]['id']) + "_" + (str)(
            photo[0]['access_key'])
    vk_session.method("messages.send",
                      {"chat_id": chat_id, "message": "", "attachment": attachment,
                       "random_id": randint(0, 2048)})

