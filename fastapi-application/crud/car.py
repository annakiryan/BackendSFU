from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from core.models import Car, Brand
from typing import Optional
from core.filters.car import CarFilter
from fastapi_pagination.ext.sqlalchemy import apaginate
from fastapi_pagination import Page


class CarCRUD:
    async def get(self, db: AsyncSession, car_id: int) -> Optional[Car]:
        stmt = select(Car).where(Car.id == car_id)
        result = await db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_all(self, db: AsyncSession, filters: CarFilter) -> Page[Car]:
        query = select(Car).join(Brand)
        query = filters.filter(query)
        query = filters.sort(query)
        return await apaginate(db, query)

    async def create(self, db: AsyncSession, car: Car) -> Car:
        db.add(car)
        await db.commit()
        await db.refresh(car)
        return car

    async def update(
        self,
        db: AsyncSession,
        car: Car,
    ) -> Car:
        await db.commit()
        await db.refresh(car)
        return car

    async def delete(self, db: AsyncSession, db_obj: Car) -> None:
        await db.delete(db_obj)
        await db.commit()


car_crud = CarCRUD()
