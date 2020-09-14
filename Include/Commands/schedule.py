from random import randint
#chat id:
#1- test bota
#2 - taverna

schedule_for_other_group = {
    1: 'photo-198707501_457239017',
    2: 'photo-198707501_457239017',
    3: None
}
def schedule(chat_id):
    try:
        return schedule_for_other_group[chat_id]
    except BaseException:
        print('траблы с расписанием')
        return None

print(schedule(2))