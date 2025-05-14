from crud.customer_car import customer_car_crud
from core.models import CustomerCar
from core.schemas.customer_car import CustomerCarCreate, CustomerCarUpdate
from sqlalchemy.ext.asyncio import AsyncSession
from core.exceptions import CustomerCarNotFound
from core.filters.customer_car import CustomerCarFilter
from fastapi_pagination import Page


class CustomerCarService:
    async def get(self, db: AsyncSession, customer_car_id: int) -> CustomerCar:
        customer_car = await customer_car_crud.get(db, customer_car_id)
        if not customer_car:
            raise CustomerCarNotFound()
        return customer_car

    async def get_all(
        self, db: AsyncSession, filters: CustomerCarFilter
    ) -> Page[CustomerCar]:
        return await customer_car_crud.get_all(db, filters)

    async def create(
        self, db: AsyncSession, customer_car_in: CustomerCarCreate
    ) -> CustomerCar:
        customer_car = CustomerCar(**customer_car_in.model_dump())
        return await customer_car_crud.create(db, customer_car)

    async def update(
        self, db: AsyncSession, customer_car_id: int, customer_car_in: CustomerCarUpdate
    ) -> CustomerCar:
        customer_car = await self.get(db, customer_car_id)
        for field, value in customer_car_in.model_dump(exclude_unset=True).items():
            setattr(customer_car, field, value)
        return await customer_car_crud.update(db, customer_car)

    async def delete(self, db: AsyncSession, customer_car_id: int) -> None:
        customer_car = await self.get(db, customer_car_id)
        await customer_car_crud.delete(db, customer_car)


customer_car_service = CustomerCarService()
