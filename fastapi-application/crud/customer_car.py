from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from core.models import CustomerCar
from core.schemas.customer_car import CustomerCarCreate
from typing import Optional
from core.filters.customer_car import CustomerCarFilter
from fastapi_pagination.ext.sqlalchemy import apaginate
from fastapi_pagination import Page


class CustomerCarCRUD:
    async def get(
        self, db: AsyncSession, customer_car_id: int
    ) -> Optional[CustomerCar]:
        stmt = select(CustomerCar).where(CustomerCar.id == customer_car_id)
        result = await db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_all(
        self, db: AsyncSession, filters: CustomerCarFilter
    ) -> Page[CustomerCar]:
        query = select(CustomerCar)
        query = filters.filter(query)
        query = filters.sort(query)
        return await apaginate(db, query)

    async def create(
        self, db: AsyncSession, customer_car: CustomerCarCreate
    ) -> CustomerCar:
        db.add(customer_car)
        await db.commit()
        await db.refresh(customer_car)
        return customer_car

    async def update(self, db: AsyncSession, customer_car: CustomerCar) -> CustomerCar:
        await db.commit()
        await db.refresh(customer_car)
        return customer_car

    async def delete(self, db: AsyncSession, customer_car: CustomerCar) -> None:
        await db.delete(customer_car)
        await db.commit()


customer_car_crud = CustomerCarCRUD()
