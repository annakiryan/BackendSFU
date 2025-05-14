from typing import Optional
from fastapi_users.schemas import BaseUser, BaseUserCreate, BaseUserUpdate
from pydantic import computed_field, Field
from .role import RoleRead
from pydantic import BaseModel
from pydantic import field_validator


class UserOnlyNameRead(BaseModel):
    id: int

    first_name: str = Field(exclude=True)
    last_name: str = Field(exclude=True)
    patronymic: Optional[str] = Field(default=None, exclude=True)

    @computed_field(return_type=str)
    @property
    def full_name(self) -> str:
        return (
            f"{self.last_name} {self.first_name} {self.patronymic}"
            if self.patronymic
            else f"{self.last_name} {self.first_name}"
        )

    class Config:
        orm_mode = True


class UserRead(BaseUser[int]):
    id: int
    email: str
    is_send_notify: bool
    role: RoleRead


class UserShortRead(BaseModel):
    id: int
    email: str

    class Config:
        orm_mode = True


class UserCreate(BaseUserCreate):
    first_name: str
    last_name: str
    patronymic: Optional[str] = None
    is_send_notify: bool = False


class UserCreateStaff(BaseUserCreate):
    first_name: str
    last_name: str
    patronymic: Optional[str] = None
    role_id: int

    @field_validator("role_id")
    def role_must_be_staff_or_admin(cls, v):
        if v not in (1, 2):
            raise ValueError("role_id must be 1 (staff) or 2 (admin)")
        return v


class UserUpdate(BaseUserUpdate):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    patronymic: Optional[str] = None
    is_send_notify: Optional[bool] = None
    role_id: Optional[int] = None
