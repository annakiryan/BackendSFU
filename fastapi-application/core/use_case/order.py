from crud.order import order_crud
from datetime import datetime
from core.models import Order, OrderStatus, User, Service
from core.schemas.order import OrderCreate, OrderAddServices, OrderRead
from core.schemas.user import UserOnlyNameRead
from core.schemas.customer_car import CustomerCarRead
from sqlalchemy.ext.asyncio import AsyncSession
from core.filters.order import OrderFilter
from datetime import timedelta
from fastapi_pagination import Page
from fastapi import BackgroundTasks
from core.services.mailing.notifications import notify_customer_if_needed
from core.exceptions import (
    OrderNotFound,
    OrderCompleted,
    ServiceNotFound,
    ServicesAlreadyAdded,
)


class OrderService:
    async def get_my_order(
        self, db: AsyncSession, order_id: int, user: User
    ) -> OrderRead:
        order = await order_crud.get_my_order(db, order_id, user)
        return await self.build_order_read(order)

    async def get(self, db: AsyncSession, order_id: int) -> OrderRead:
        order = await self.get_order_from_db(db, order_id)
        return await self.build_order_read(order)

    async def get_order_services(
        self, db: AsyncSession, order_id: int, user: User
    ) -> Page[Service]:
        return await order_crud.get_order_services(db, order_id, user)

    async def get_all(
        self, db: AsyncSession, filters: OrderFilter, user: User
    ) -> Page[Order]:
        return await order_crud.get_all(db, filters, user)

    async def create(
        self, db: AsyncSession, order_in: OrderCreate, admin_id: int
    ) -> OrderRead:
        new_order = Order(
            administrator_id=admin_id,
            employee_id=order_in.employee_id,
            customer_car_id=order_in.customer_car_id,
        )
        new_order = await order_crud.create(db, new_order)

        services = await order_crud.get_services_by_ids(db, order_in.services)
        new_order.services.extend(services)

        total_time = sum(s.time.seconds for s in services)
        new_order.end_date = new_order.start_date + timedelta(seconds=total_time)

        updated_order = await order_crud.update(db, new_order)
        return await self.build_order_read(updated_order)

    async def update(
        self, db: AsyncSession, order_id: int, order_in: OrderAddServices
    ) -> OrderRead:
        order = await self.get_order_from_db(db, order_id)

        if order.status != OrderStatus.IN_PROGRESS:
            raise OrderCompleted()

        existing_service_ids = {service.id for service in order.services}
        requested_service_ids = set(order_in.services)

        already_added_ids = list(existing_service_ids & requested_service_ids)
        service_ids_to_add = list(requested_service_ids - existing_service_ids)

        if already_added_ids:
            raise ServicesAlreadyAdded(already_added_ids)

        if not service_ids_to_add:
            raise ServiceNotFound()

        services_to_add = await order_crud.get_services_by_ids(db, service_ids_to_add)
        if not services_to_add:
            raise ServiceNotFound()

        order.services.extend(services_to_add)

        additional_time = sum(s.time.seconds for s in services_to_add)
        order.end_date = order.end_date + timedelta(seconds=additional_time)

        updated_order = await order_crud.update(db, order)
        return await self.build_order_read(updated_order)

    async def delete(self, db: AsyncSession, order_id: int) -> None:
        order = await self.get_order_from_db(db, order_id)
        await order_crud.delete(db, order)

    async def update_status(
        self, db: AsyncSession, order_id: int, background_tasks: BackgroundTasks
    ) -> Order:
        order = await self.get_order_from_db(db, order_id)
        if order.status == OrderStatus.COMPLETED:
            raise OrderCompleted()

        order.status = OrderStatus.COMPLETED
        order.end_date = datetime.now()
        updated_order = await order_crud.update_status(db, order)

        notify_customer_if_needed(order, background_tasks)
        return await self.build_order_read(updated_order)

    async def get_order_from_db(self, db: AsyncSession, order_id: int) -> Order:
        order = await order_crud.get(db, order_id)
        if not order:
            raise OrderNotFound()
        return order

    async def build_order_read(self, order: Order) -> OrderRead:
        total_price = sum(service.price.max_value for service in order.services)
        total_time = sum(service.time.minute for service in order.services)
        order_read = OrderRead.model_validate(order, from_attributes=True)

        order_read.total_price = total_price
        order_read.total_time = total_time

        return order_read


order_service = OrderService()
