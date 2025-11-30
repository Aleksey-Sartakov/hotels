

class MainException(Exception):
    details = "Неизвестная ошибка!"

    def __init__(self, *args, **kwargs):
        super().__init__(self.details, *args, **kwargs)


class ObjectNotFoundException(MainException):
    details = "Объект не найден!"


class AllRoomsAreBookedException(MainException):
    details = "Не осталось свободных номеров!"


class DBRestrictionsViolatedException(MainException):
    details = "Нарушены ограничения БД при добавлении новых данных."


class DateToIsLessOrEqualThenDateFromException(MainException):
    details = "Дата конца меньше или равна дате начала."
