from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from core.config import settings
from core.schemas.service import ServiceCreate, ServiceUpdate, ServiceRead
from core.use_case.service import service_service
from core.exceptions import ServiceNotFound
from core.models import db_helper
from core.filters.service import ServiceFilter
from fastapi_filter import FilterDepends
from fastapi_pagination import Page
from api.dependencies.authentication.role_check import get_current_admin_user

router = APIRouter(prefix=settings.api.v1.services, tags=["Services"])


@router.get(
    "/",
    response_model=Page[ServiceRead],
    dependencies=[Depends(get_current_admin_user)],
)
async def get_all_services(
    service_filter: ServiceFilter = FilterDepends(ServiceFilter),
    db: AsyncSession = Depends(db_helper.session_getter),
):
    try:
        return await service_service.get_all(db, service_filter)
    except NotImplementedError as e:
        if "asc_op" in str(e):
            raise HTTPException(
                status_code=400, detail="Сортировка по этому полю невозможна."
            )
        raise e


@router.get(
    "/{service_id}",
    response_model=ServiceRead,
    dependencies=[Depends(get_current_admin_user)],
)
async def get_service(
    service_id: int, db: AsyncSession = Depends(db_helper.session_getter)
):
    try:
        return await service_service.get(db, service_id)
    except ServiceNotFound:
        raise HTTPException(status_code=404, detail="Услуга не найдена")


@router.post(
    "/",
    response_model=ServiceRead,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(get_current_admin_user)],
)
async def create_service(
    service_in: ServiceCreate, db: AsyncSession = Depends(db_helper.session_getter)
):
    return await service_service.create(db, service_in)


@router.put(
    "/{service_id}",
    response_model=ServiceRead,
    dependencies=[Depends(get_current_admin_user)],
)
async def replace_service(
    service_id: int,
    service_in: ServiceCreate,
    db: AsyncSession = Depends(db_helper.session_getter),
):
    try:
        return await service_service.update(db, service_id, service_in)
    except ServiceNotFound:
        raise HTTPException(status_code=404, detail="Услуга не найдена")


@router.patch(
    "/{service_id}",
    response_model=ServiceRead,
    dependencies=[Depends(get_current_admin_user)],
)
async def update_service(
    service_id: int,
    service_in: ServiceUpdate,
    db: AsyncSession = Depends(db_helper.session_getter),
):
    try:
        return await service_service.update(db, service_id, service_in)
    except ServiceNotFound:
        raise HTTPException(status_code=404, detail="Услуга не найдена")


@router.delete(
    "/{service_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(get_current_admin_user)],
)
async def delete_service(
    service_id: int, db: AsyncSession = Depends(db_helper.session_getter)
):
    try:
        await service_service.delete(db, service_id)
    except ServiceNotFound:
        raise HTTPException(status_code=404, detail="Услуга не найдена")
