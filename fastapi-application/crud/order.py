from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from fastapi_pagination.ext.sqlalchemy import apaginate
from fastapi_pagination import Page
from typing import Optional

from core.models import Order, Service, User, CustomerCar, OrderService
from core.filters.order import OrderFilter
from core.exceptions import PermissionDenied, OrderNotFound


class OrderCRUD:
    async def _apply_user_filter(self, stmt, user: User):
        match user.role.name:
            case "admin":
                return stmt
            case "customer":
                return stmt.join(Order.customer_car).where(
                    CustomerCar.customer_id == user.id
                )
            case "employee":
                return stmt.where(Order.employee_id == user.id)
            case _:
                raise PermissionDenied()

    async def get_my_order(
        self, db: AsyncSession, order_id: int, user: User
    ) -> Optional[Order]:
        stmt = (
            select(Order)
            .options(selectinload(Order.services))
            .where(Order.id == order_id)
        )
        stmt = await self._apply_user_filter(stmt, user)

        result = await db.execute(stmt)
        order = result.scalar()

        if not order:
            raise PermissionDenied()

        return order

    async def get(self, db: AsyncSession, order_id: int) -> Optional[Order]:
        stmt = select(Order).where(Order.id == order_id)
        result = await db.execute(stmt)
        return result.scalar()

    async def get_order_services(
        self, db: AsyncSession, order_id: int, user: User
    ) -> Page[Service]:
        stmt_check = select(Order).where(Order.id == order_id)
        stmt_check = await self._apply_user_filter(stmt_check, user)

        result = await db.execute(stmt_check)
        if not result.scalar():
            raise OrderNotFound()

        stmt = (
            select(Service)
            .join(OrderService)
            .join(Order)
            .where(Order.id == order_id)
        )
        return await apaginate(db, stmt)

    async def get_all(
        self, db: AsyncSession, filters: OrderFilter, user: User
    ) -> Page[Order]:
        stmt = select(Order).options(selectinload(Order.services))
        stmt = await self._apply_user_filter(stmt, user)

        stmt = filters.filter(stmt)
        stmt = filters.sort(stmt)

        return await apaginate(db, stmt)

    async def create(self, db: AsyncSession, order: Order) -> Order:
        db.add(order)
        await db.commit()
        await db.refresh(order)
        return order

    async def update(self, db: AsyncSession, order: Order) -> Order:
        await db.commit()
        await db.refresh(order)
        return order

    async def delete(self, db: AsyncSession, db_obj: Order) -> None:
        await db.delete(db_obj)
        await db.commit()

    async def update_status(self, db: AsyncSession, order: Order) -> Order:
        await db.commit()
        await db.refresh(order)
        return order

    async def get_services_by_ids(
        self, db: AsyncSession, ids: list[int]
    ) -> list[Service]:
        stmt = select(Service).where(Service.id.in_(ids))
        result = await db.execute(stmt)
        return result.scalars().all()


order_crud = OrderCRUD()
