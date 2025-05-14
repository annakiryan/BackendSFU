from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional
from core.models.brand import Brand
from core.filters.brand import BrandFilter
from fastapi_pagination.ext.sqlalchemy import apaginate
from fastapi_pagination import Page


class BrandCRUD:
    async def get_all(
        self, db: AsyncSession, filters: BrandFilter
    ) -> Page[Brand]:
        stmt = select(Brand)
        stmt = filters.filter(stmt)
        return await apaginate(db, stmt)

    async def get(self, db: AsyncSession, brand_id: int) -> Optional[Brand]:
        stmt = select(Brand).where(Brand.id == brand_id)
        result = await db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_name(self, db: AsyncSession, name: str) -> Optional[Brand]:
        stmt = select(Brand).where(Brand.name == name)
        result = await db.execute(stmt)
        return result.scalar_one_or_none()

    async def create(self, db: AsyncSession, brand: Brand) -> Brand:
        db.add(brand)
        await db.commit()
        await db.refresh(brand)
        return brand

    async def update(
        self,
        db: AsyncSession,
        brand: Brand,
    ) -> Brand:
        await db.commit()
        await db.refresh(brand)
        return brand

    async def delete(self, db: AsyncSession, brand: Brand) -> None:
        await db.delete(brand)
        await db.commit()


brand_crud = BrandCRUD()
