from typing import Optional, TYPE_CHECKING
from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from .base import Base

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


class User(SQLAlchemyBaseUserTable[int], Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(nullable=False)
    last_name: Mapped[str] = mapped_column(nullable=False)
    patronymic: Mapped[Optional[str]] = mapped_column(nullable=True)
    is_send_notify: Mapped[bool] = mapped_column(default=False, nullable=False)
    role_id: Mapped[int] = mapped_column(ForeignKey("roles.id"), nullable=False, default=3)

    role: Mapped["Role"] = relationship(back_populates="users", lazy="joined")

    cars: Mapped[list["CustomerCar"]] = relationship(
        back_populates="customer", cascade="all, delete-orphan", lazy="selectin"
    )

    @classmethod
    def get_db(cls, session: "AsyncSession"):
        from core.authentication.user_db import CustomUserDatabase
        return CustomUserDatabase(session, cls)
