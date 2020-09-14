def get_commands():
    commands = "Доступны следующие команды:\n" +\
               "help, команды, помощь - для вызова этой документации\n" \
               "/slash - вкл/выкл обращений к командам через /. Если функция включена," \
               "то распознование команд будет только если в начале сообщения поставить /. " \
               "если отключена, то можно без него\n" \
               "погода - для вызова погоды на сегодня\n" \
               "погода завтра - для вызова погоды на завтра\n" \
               "расписание - для получения фотографии расписания\n" \
               "аниме - пажилая пушка\n" \
               "неделя - для получения информации о неделе (под чертой или над чертой)\n" \
               "перестрелка @id - для того шобы пастреляца\n" \
               "roll или ролл <меньшее число>,< большее число> \n" \
               "dice или кубик - для бросока кубика\n" \
               "flip, монетка или coin - для подкидывания монетки\n" \
               "cinema, film, films или кино - для вывода 3 случайных фильмов\n"
    return commands
