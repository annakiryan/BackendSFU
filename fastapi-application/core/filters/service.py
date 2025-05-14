from typing import Optional
from fastapi_filter.contrib.sqlalchemy import Filter
from core.models import Service
from core.utils.converters import PriceConverter, TimeConverter


class ServiceFilter(Filter):
    name: Optional[str] = None
    price_in_coins__lt: Optional[int] = None
    price_in_coins__gt: Optional[int] = None
    time_in_seconds__lte: Optional[int] = None
    time_in_seconds__gte: Optional[int] = None
    order_by: Optional[list[str]] = ["price_in_coins", "time_in_seconds", "name"]

    class Constants(Filter.Constants):
        model = Service

    def to_internal(self) -> "ServiceFilter":
        if self.price_in_coins__lt is not None:
            self.price_in_coins__lt = PriceConverter.rub_to_coins(
                self.price_in_coins__lt
            )
        if self.price_in_coins__gt is not None:
            self.price_in_coins__gt = PriceConverter.rub_to_coins(
                self.price_in_coins__gt
            )
        if self.time_in_seconds__lte is not None:
            self.time_in_seconds__lte = TimeConverter.min_to_sec(
                self.time_in_seconds__lte
            )
        if self.time_in_seconds__gte is not None:
            self.time_in_seconds__gte = TimeConverter.min_to_sec(
                self.time_in_seconds__gte
            )
        return self
