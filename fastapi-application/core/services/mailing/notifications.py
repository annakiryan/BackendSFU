from core.utils.mail import send_email_to_customer
from core.models.order import Order
import logging
from datetime import datetime

logger = logging.getLogger(__name__)


async def notify_customer_if_needed(order: Order) -> None:
    customer = order.customer_car.customer
    if customer.is_send_notify:
        try:
            await send_email_to_customer(
                email=customer.email,
                subject="Ваш заказ выполнен",
                message=f"Здравствуйте! Ваш заказ №{order.id} был успешно выполнен.",
            )
        except Exception as e:
            logger.error(
                f"{datetime.now()} Не удалось отправить письмо клиенту {customer.email}: {e}"
            )
