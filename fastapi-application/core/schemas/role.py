from pydantic import BaseModel, ConfigDict
from typing import Optional


class RoleBase(BaseModel):
    name: str


class RoleCreate(RoleBase):
    pass


class RoleRead(RoleBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class RoleUpdate(BaseModel):
    name: Optional[str]
