from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base


class Role(Base):
    __tablename__ = "roles"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)

    users: Mapped[list["User"]] = relationship(back_populates="role", lazy="selectin")
