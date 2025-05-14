from typing import Optional
from pydantic import BaseModel
from pydantic.config import ConfigDict


class BrandBase(BaseModel):
    name: str


class BrandCreate(BrandBase):
    pass


class BrandRead(BrandBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class BrandOnlyNameRead(BrandBase):
    pass


class BrandUpdate(BaseModel):
    name: Optional[str] = None
