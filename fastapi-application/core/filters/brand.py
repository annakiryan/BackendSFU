from typing import Optional
from fastapi_filter.contrib.sqlalchemy import Filter
from core.models import Brand


class BrandFilter(Filter):
    name: Optional[str] = None

    class Constants(Filter.Constants):
        model = Brand
