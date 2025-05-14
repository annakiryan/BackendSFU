from datetime import datetime
from sqlalchemy import ForeignKey, DateTime, Integer, text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base
import enum


class OrderStatus(enum.IntEnum):
    IN_PROGRESS = 0
    COMPLETED = 1


class Order(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(primary_key=True)

    administrator_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"), nullable=False
    )
    employee_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    customer_car_id: Mapped[int] = mapped_column(
        ForeignKey("customer_cars.id"), nullable=False
    )

    status: Mapped[OrderStatus] = mapped_column(
        Integer, default=OrderStatus.IN_PROGRESS, nullable=False
    )

    start_date: Mapped[datetime] = mapped_column(
        DateTime, server_default=text("CURRENT_TIMESTAMP"), nullable=False
    )
    end_date: Mapped[datetime] = mapped_column(DateTime, nullable=True)

    administrator: Mapped["User"] = relationship(
        foreign_keys=[administrator_id], lazy="joined"
    )
    employee: Mapped["User"] = relationship(foreign_keys=[employee_id], lazy="joined")
    customer_car: Mapped["CustomerCar"] = relationship(lazy="joined")

    services: Mapped[list["Service"]] = relationship(
        secondary="order_service", back_populates="orders", lazy="selectin"
    )

    @property
    def total_price(self) -> int:
        return sum(service.price.max_value for service in self.services)

    @property
    def total_time(self) -> int:
        return sum(service.time.minute for service in self.services)
