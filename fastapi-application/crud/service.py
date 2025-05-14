from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from core.models import Service
from typing import Optional
from core.filters.service import ServiceFilter
from fastapi_pagination.ext.sqlalchemy import apaginate
from fastapi_pagination import Page


class ServiceCRUD:
    async def get(self, db: AsyncSession, service_id: int) -> Optional[Service]:
        stmt = select(Service).where(Service.id == service_id)
        result = await db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_all(
        self, db: AsyncSession, service_filter: ServiceFilter
    ) -> Page[Service]:
        query = select(Service)
        query = service_filter.filter(query)
        query = service_filter.sort(query)
        return await apaginate(db, query)

    async def create(self, db: AsyncSession, service: Service) -> Service:
        db.add(service)
        await db.commit()
        await db.refresh(service)
        return service

    async def update(
        self,
        db: AsyncSession,
        service: Service,
    ) -> Service:
        await db.commit()
        await db.refresh(service)
        return service

    async def delete(self, db: AsyncSession, service: Service) -> None:
        await db.delete(service)
        await db.commit()


service_crud = ServiceCRUD()
