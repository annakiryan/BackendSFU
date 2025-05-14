from typing import Optional
from fastapi_filter import FilterDepends, with_prefix
from fastapi_filter.contrib.sqlalchemy import Filter
from pydantic import Field
from core.models import Car
from core.filters.brand import BrandFilter


class CarFilter(Filter):
    brand: Optional[BrandFilter] = FilterDepends(with_prefix("brand", BrandFilter))

    order_by: Optional[list[str]] = Field(
        default=None,
    )

    class Constants(Filter.Constants):
        model = Car
