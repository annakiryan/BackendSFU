from pydantic import BaseModel
from typing import Optional
from .car import CarRead
from .user import UserShortRead
from pydantic.config import ConfigDict


class CustomerCarBase(BaseModel):
    year: int
    number: str


class CustomerCarCreate(CustomerCarBase):
    customer_id: int
    car_id: int


class CustomerCarRead(CustomerCarBase):
    id: int
    customer: UserShortRead
    car: CarRead

    model_config = ConfigDict(from_attributes=True)


class CustomerCarUpdate(BaseModel):
    year: Optional[int] = None
    number: Optional[str] = None
    customer_id: Optional[int] = None
    car_id: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)
