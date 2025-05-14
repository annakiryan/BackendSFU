from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional
from uuid import UUID
from .base import Base


class CustomerCar(Base):
    __tablename__ = "customer_cars"

    id: Mapped[int] = mapped_column(primary_key=True)
    customer_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    car_id: Mapped[int] = mapped_column(
        ForeignKey("cars.id", ondelete="CASCADE"), nullable=False
    )

    year: Mapped[int] = mapped_column(Integer, nullable=False)
    number: Mapped[str] = mapped_column(String(20), nullable=False)

    customer: Mapped["User"] = relationship(back_populates="cars", lazy="joined")
    car: Mapped["Car"] = relationship(back_populates="customer_cars", lazy="joined")

    def __repr__(self):
        return f"<CustomerCar {self.car_id} ({self.number})>"
