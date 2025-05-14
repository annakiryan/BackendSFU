from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, PrivateAttr, conlist
from .user import UserOnlyNameRead
from .customer_car import CustomerCarRead
from .service import ServiceRead


class OrderCreate(BaseModel):
    employee_id: int
    customer_car_id: int
    services: conlist(int, min_length=1)


class OrderRead(BaseModel):
    id: int
    status: int
    start_date: datetime
    end_date: datetime | None
    total_price: int | None = None
    total_time: int | None = None
    administrator: UserOnlyNameRead
    employee: UserOnlyNameRead | None = None
    customer_car: CustomerCarRead
    _services: List[ServiceRead] = PrivateAttr(default_factory=list)

    class Config:
        from_attributes = True
        json_encoders = {
            datetime: lambda dt: dt.strftime("%Y-%m-%d %H:%M:%S"),
        }


class OrderAddServices(BaseModel):
    services: List[int]


class OrderComplete(BaseModel):
    pass
