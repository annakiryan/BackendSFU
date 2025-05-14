from pydantic import BaseModel
from pydantic.config import ConfigDict
from typing import Optional
from .brand import BrandOnlyNameRead


class CarBase(BaseModel):
    model: str


class CarCreate(CarBase):
    brand_id: Optional[int] = None
    brand_name: Optional[str] = None


class CarRead(CarBase):
    id: int
    brand: BrandOnlyNameRead

    model_config = ConfigDict(from_attributes=True)


class CarUpdate(BaseModel):
    model: Optional[str] = None
    brand_id: Optional[int] = None
    brand_name: Optional[str] = None


class CarFilter(BaseModel):
    brand: Optional[str] = None
