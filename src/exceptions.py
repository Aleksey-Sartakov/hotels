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


class FacilitiesNotFoundException(ObjectNotFoundException):
    details = "Удобства не найдены!"
    ids: list[int] = None

    def __init__(self, ids: list[int]):
        self.ids = ids
        super().__init__()


class AllRoomsAreBookedException(MainException):
    details = "Не осталось свободных номеров!"


class SameObjectAlreadyExistsException(MainException):
    details = "Нарушены ограничения БД при добавлении новых данных."


class DateToLessOrEqualThenDateFromException(MainException):
    details = "Дата конца меньше или равна дате начала."


class DateCannotBeInPastException(MainException):
    details = "Дата не может быть установлена в прошлом. Она должна быть больше или равна текущей."


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


class FacilitiesNotFoundHTTPException(MainHTTPException):
    status_code = status.HTTP_404_NOT_FOUND

    def __init__(self, ids: list[int]):
        self.detail = {"message": "Удобства не найдены!", "ids": ids}
        super().__init__()


class DateCannotBeInPastHTTPException(MainHTTPException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Дата не может быть установлена в прошлом. Она должна быть больше или равна текущей."


class BookingDateToLessOrEqualThenDateFromHTTPException(MainHTTPException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Дата выезда должна быть указана позднее даты заезда."
