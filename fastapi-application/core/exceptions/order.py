from fastapi import HTTPException


class OrderNotFound(Exception):
    pass


class OrderCompleted(Exception):
    pass


class ServicesAlreadyAdded(HTTPException):
    def __init__(self, service_ids: list[int]):
        super().__init__(
            status_code=400,
            detail={
                "error": "Некоторые из выбранных услуг уже добавлены в заказ",
                "already_added_service_ids": service_ids,
            },
        )


class ServicesNotFound(Exception):
    pass
