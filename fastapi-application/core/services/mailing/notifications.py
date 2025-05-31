from core.utils.mail import send_email_wrapper
from core.models.order import Order
import logging
from fastapi import BackgroundTasks

logger = logging.getLogger(__name__)


def notify_customer(order: Order, background_tasks: BackgroundTasks) -> None:
    customer = order.customer_car.customer
    background_tasks.add_task(
        send_email_wrapper,
        customer.email,
        "Ваш заказ выполнен",
        f"Здравствуйте! Ваш заказ №{order.id} был успешно выполнен.",
    )
