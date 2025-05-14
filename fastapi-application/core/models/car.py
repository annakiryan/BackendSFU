from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String
from .base import Base


class Car(Base):
    __tablename__ = "cars"

    id: Mapped[int] = mapped_column(primary_key=True)
    brand_id: Mapped[int] = mapped_column(ForeignKey("brand.id"), nullable=False)
    model: Mapped[str] = mapped_column(String(100), nullable=False)

    customer_cars: Mapped[list["CustomerCar"]] = relationship(
        back_populates="car", cascade="all, delete-orphan", lazy="selectin"
    )
    brand: Mapped["Brand"] = relationship(back_populates="cars", lazy="joined")
