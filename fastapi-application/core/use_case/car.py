from crud.car import car_crud
from core.models import Car
from core.schemas.car import CarCreate, CarUpdate
from core.use_case.brand import brand_service
from sqlalchemy.ext.asyncio import AsyncSession
from core.exceptions import CarNotFound, BrandRequired, BrandAlreadyExists, OnlyOneWayToCreateBrand
from core.filters.car import CarFilter
from fastapi_pagination import Page


class CarService:
    async def get(self, db: AsyncSession, car_id: int) -> Car:
        car = await car_crud.get(db, car_id)
        if not car:
            raise CarNotFound()
        return car

    async def get_all(self, db: AsyncSession, filters: CarFilter) -> Page[Car]:
        return await car_crud.get_all(db, filters)

    async def create(self, db: AsyncSession, car_in: CarCreate) -> Car:
        brand_id = await self._resolve_brand(db, car_in.brand_id, car_in.brand_name)
        car_data = car_in.model_dump(exclude={"brand_name"})
        car = Car(**car_data)
        car.brand_id = brand_id
        return await car_crud.create(db, car)

    async def update(self, db: AsyncSession, car_id: int, car_in: CarUpdate) -> Car:
        car = await self.get(db, car_id)

        if car_in.brand_id is not None or car_in.brand_name is not None:
            brand_id = await self._resolve_brand(db, car_in.brand_id, car_in.brand_name)
            car.brand_id = brand_id

        for field, value in car_in.model_dump(
            exclude_unset=True, exclude={"brand_name", "brand_id"}
        ).items():
            setattr(car, field, value)
        return await car_crud.update(db, car)

    async def delete(self, db: AsyncSession, car_id: int) -> None:
        car = await car_crud.get(db, car_id)
        await car_crud.delete(db, car)

    async def _resolve_brand(
        self, db: AsyncSession, brand_id: int | None, brand_name: str | None
    ) -> int:
        if brand_id and brand_name:
            raise OnlyOneWayToCreateBrand()

        if brand_id:
            return brand_id

        if brand_name:
            existing_brand = await brand_service.get_by_name(db, brand_name)
            if existing_brand:
                raise BrandAlreadyExists()

            new_brand = await brand_service.create(db, brand_name)
            return new_brand.id

        raise BrandRequired()


car_service = CarService()
