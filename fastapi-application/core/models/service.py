from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, composite, relationship
from .base import Base
from core.value_objects import PriceVO, TimeVO


class Service(Base):
    __tablename__ = "services"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)

    price_in_coins: Mapped[int] = mapped_column(Integer, nullable=False)
    time_in_seconds: Mapped[int] = mapped_column(Integer, nullable=False)

    price: Mapped[PriceVO] = composite(PriceVO, "price_in_coins")
    time: Mapped[TimeVO] = composite(TimeVO, "time_in_seconds")

    orders: Mapped[list["Order"]] = relationship(
        secondary="order_service", back_populates="services", lazy="selectin"
    )
