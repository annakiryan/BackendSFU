from typing import Optional
from fastapi_filter.contrib.sqlalchemy import Filter
from pydantic import Field
from core.models import Order
from datetime import datetime


class OrderFilter(Filter):
    status: Optional[int] = None
    start_date__gte: datetime | None = None
    start_date__lte: datetime | None = None
    end_date__gte: datetime | None = None
    end_date__lte: datetime | None = None

    order_by: Optional[list[str]] = Field(
        default=None,
    )

    class Constants(Filter.Constants):
        model = Order
