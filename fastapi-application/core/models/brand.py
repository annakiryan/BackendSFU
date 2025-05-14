from sqlalchemy import String
from sqlalchemy.orm import mapped_column, Mapped, relationship
from .base import Base


class Brand(Base):
    __tablename__ = "brand"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)

    cars: Mapped[list["Car"]] = relationship(
        back_populates="brand", cascade="all, delete-orphan", lazy="selectin"
    )
