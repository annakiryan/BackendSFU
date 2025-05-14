from crud.service import service_crud
from core.models import Service
from core.value_objects import PriceVO, TimeVO
from core.schemas.service import ServiceCreate, ServiceUpdate
from sqlalchemy.ext.asyncio import AsyncSession
from core.exceptions import ServiceNotFound
from core.filters.service import ServiceFilter
from fastapi_pagination import Page


class ServiceService:
    async def get(self, db: AsyncSession, service_id: int) -> Service:
        service = await service_crud.get(db, service_id)
        if not service:
            raise ServiceNotFound()
        return service

    async def get_all(
        self, db: AsyncSession, service_filter: ServiceFilter
    ) -> Page[Service]:
        return await service_crud.get_all(db, service_filter.to_internal())

    async def create(self, db: AsyncSession, service_in: ServiceCreate) -> Service:
        internal_data = service_in.to_internal()
        price_vo = PriceVO(internal_data["price"])
        time_vo = TimeVO(internal_data["time"])

        service = Service(name=internal_data["name"], price=price_vo, time=time_vo)
        return await service_crud.create(db, service)

    async def update(
        self, db: AsyncSession, service_id: int, service_in: ServiceUpdate
    ) -> Service:
        service = await self.get(db, service_id)
        internal_data = service_in.to_internal()
        if "price" in internal_data:
            service.price = PriceVO(internal_data["price"])
        if "time" in internal_data:
            service.time = TimeVO(internal_data["time"])
        for field, value in internal_data.items():
            if field in ("price", "time"):
                continue
            setattr(service, field, value)
        return await service_crud.update(db, service)

    async def delete(self, db: AsyncSession, service_id: int) -> None:
        service = await service_crud.get(db, service_id)
        if not service:
            raise ServiceNotFound()
        await service_crud.delete(db, service)


service_service = ServiceService()
