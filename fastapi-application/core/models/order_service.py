from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column
from .base import Base


class OrderService(Base):
    __tablename__ = "order_service"

    id: Mapped[int] = mapped_column(primary_key=True)

    order_id: Mapped[int] = mapped_column(
        ForeignKey("orders.id", ondelete="CASCADE"), nullable=False
    )
    service_id: Mapped[int] = mapped_column(
        ForeignKey("services.id", ondelete="CASCADE"), nullable=False
    )
