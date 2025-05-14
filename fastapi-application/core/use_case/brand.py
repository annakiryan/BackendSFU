from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from core.schemas.brand import BrandCreate, BrandUpdate
from core.models.brand import Brand
from crud.brand import brand_crud
from core.exceptions.brand import BrandAlreadyExists, BrandNotFound
from core.filters.brand import BrandFilter
from fastapi_pagination import Page


class BrandService:
    async def get_all(self, db: AsyncSession, filters: BrandFilter) -> Page[Brand]:
        return await brand_crud.get_all(db, filters)

    async def get(self, db: AsyncSession, brand_id: int) -> Brand:
        brand = await brand_crud.get(db, brand_id)
        if not brand:
            raise BrandNotFound()
        return brand

    async def get_by_name(self, db: AsyncSession, brand_name: str) -> Optional[Brand]:
        return await brand_crud.get_by_name(db, brand_name)

    async def create(self, db: AsyncSession, brand_in: BrandCreate) -> Brand:
        await self._check_name_not_exists(db, brand_in.name)
        brand = Brand(**brand_in.model_dump())
        return await brand_crud.create(db, brand)

    async def update(
        self, db: AsyncSession, brand_id: int, brand_in: BrandUpdate
    ) -> Brand:
        brand = await self.get(db, brand_id)

        if brand_in.name and brand_in.name != brand.name:
            await self._check_name_not_exists(db, brand_in.name)

        for field, value in brand_in.model_dump(exclude_unset=True).items():
            setattr(brand, field, value)

        return await brand_crud.update(db, brand)

    async def delete(self, db: AsyncSession, brand_id: int) -> None:
        brand = await self.get(db, brand_id)
        await brand_crud.delete(db, brand)

    async def _check_name_not_exists(self, db: AsyncSession, name: str) -> None:
        existing = await brand_crud.get_by_name(db, name)
        if existing:
            raise BrandAlreadyExists()


brand_service = BrandService()
