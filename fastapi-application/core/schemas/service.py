from typing import Optional
from pydantic import BaseModel, Field, model_validator, field_validator


class PriceInput(BaseModel):
    rubles: int = Field(..., ge=0, example=150)


class TimeInput(BaseModel):
    minutes: int = Field(..., ge=0, example=30)


class ServiceCreate(BaseModel):
    name: str
    price: PriceInput
    time: TimeInput

    def to_internal(self):
        return {
            "name": self.name,
            "price": self.price.rubles * 100,
            "time": self.time.minutes * 60,
        }


class ServiceUpdate(BaseModel):
    name: Optional[str] = None
    price: Optional[PriceInput] = None
    time: Optional[TimeInput] = None

    def to_internal(self):
        data = {}
        if self.name is not None:
            data["name"] = self.name
        if self.price is not None:
            data["price"] = self.price.rubles * 100
        if self.time is not None:
            data["time"] = self.time.minutes * 60
        return data


class PriceVORead(BaseModel):
    minValue: int
    maxValue: int
    format: str


class TimeVORead(BaseModel):
    second: int
    minute: int


class ServiceRead(BaseModel):
    id: int
    name: str
    price: PriceVORead
    time: TimeVORead

    class Config:
        from_attributes = True

    @model_validator(mode="before")
    @classmethod
    def map_composites(cls, service):
        if isinstance(service, dict):
            return service

        return {
            "id": service.id,
            "name": service.name,
            "price": PriceVORead(
                minValue=service.price.min_value,
                maxValue=service.price.max_value,
                format=service.price.format,
            ),
            "time": TimeVORead(
                second=service.time.second,
                minute=service.time.minute,
            ),
        }
