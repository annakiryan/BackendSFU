from typing import Optional
from fastapi_filter.contrib.sqlalchemy import Filter
from pydantic import Field
from core.models import CustomerCar


class CustomerCarFilter(Filter):
    year__gt: Optional[int] = None
    year__lt: Optional[int] = None

    order_by: Optional[list[str]] = Field(
        default=None,
    )

    class Constants(Filter.Constants):
        model = CustomerCar
