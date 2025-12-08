from fastapi import HTTPException
from starlette import status


class MainException(Exception):
    details = "Неизвестная ошибка!"

    def __init__(self, *args, **kwargs):
        super().__init__(self.details, *args, **kwargs)


class ObjectNotFoundException(MainException):
    details = "Объект не найден!"


class HotelNotFoundException(ObjectNotFoundException):
    details = "Отель не найден!"


class RoomNotFoundException(ObjectNotFoundException):
    details = "Номер не найден!"


class AllRoomsAreBookedException(MainException):
    details = "Не осталось свободных номеров!"


class SameObjectAlreadyExistsException(MainException):
    details = "Нарушены ограничения БД при добавлении новых данных."


class DateToLessOrEqualThenDateFromException(MainException):
    details = "Дата конца меньше или равна дате начала."


class MainHTTPException(HTTPException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail = "Неизвестная ошибка!"

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class HotelNotFoundHTTPException(MainHTTPException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Отель не найден"


class RoomNotFoundHTTPException(MainHTTPException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Номер не найден"
