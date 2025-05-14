from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from core.config import settings
from core.schemas.customer_car import (
    CustomerCarCreate,
    CustomerCarRead,
    CustomerCarUpdate,
)
from core.use_case.customer_car import customer_car_service
from core.exceptions import CustomerCarNotFound
from core.models import db_helper
from core.filters.customer_car import CustomerCarFilter
from fastapi_filter import FilterDepends
from fastapi_pagination import Page
from api.dependencies.authentication.role_check import get_current_admin_user

router = APIRouter(prefix=settings.api.v1.customer_cars, tags=["Customer cars"])


@router.get(
    "/",
    response_model=Page[CustomerCarRead],
    dependencies=[Depends(get_current_admin_user)],
)
async def get_all_customer_cars(
    customer_car_filter: CustomerCarFilter = FilterDepends(CustomerCarFilter),
    db: AsyncSession = Depends(db_helper.session_getter),
):
    try:
        return await customer_car_service.get_all(db, customer_car_filter)
    except NotImplementedError as e:
        if "asc_op" in str(e):
            raise HTTPException(
                status_code=400, detail="Сортировка по этому полю невозможна."
            )
        raise e


@router.get(
    "/{customer_car_id}",
    response_model=CustomerCarRead,
    dependencies=[Depends(get_current_admin_user)],
)
async def get_customer_car(
    customer_car_id: int, db: AsyncSession = Depends(db_helper.session_getter)
):
    try:
        return await customer_car_service.get(db, customer_car_id)
    except CustomerCarNotFound:
        raise HTTPException(
            status_code=404, detail="Машина этого покупателя не найдена"
        )


@router.post(
    "/",
    response_model=CustomerCarRead,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(get_current_admin_user)],
)
async def create_customer_car(
    customer_car_in: CustomerCarCreate,
    db: AsyncSession = Depends(db_helper.session_getter),
):
    return await customer_car_service.create(db, customer_car_in)


@router.put(
    "/{customer_car_id}",
    response_model=CustomerCarRead,
    dependencies=[Depends(get_current_admin_user)],
)
async def replace_customer_car(
    customer_car_id: int,
    customer_car_in: CustomerCarCreate,
    db: AsyncSession = Depends(db_helper.session_getter),
):
    try:
        return await customer_car_service.update(db, customer_car_id, customer_car_in)
    except CustomerCarNotFound:
        raise HTTPException(
            status_code=404, detail="Машина этого покупателя не найдена"
        )


@router.patch(
    "/{customer_car_id}",
    response_model=CustomerCarRead,
    dependencies=[Depends(get_current_admin_user)],
)
async def update_customer_car(
    customer_car_id: int,
    customer_car_in: CustomerCarUpdate,
    db: AsyncSession = Depends(db_helper.session_getter),
):
    try:
        return await customer_car_service.update(db, customer_car_id, customer_car_in)
    except CustomerCarNotFound:
        raise HTTPException(
            status_code=404, detail="Машина этого покупателя не найдена"
        )


@router.delete(
    "/{customer_car_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(get_current_admin_user)],
)
async def delete_customer_car(
    customer_car_id: int, db: AsyncSession = Depends(db_helper.session_getter)
):
    try:
        await customer_car_service.delete(db, customer_car_id)
    except CustomerCarNotFound:
        raise HTTPException(
            status_code=404, detail="Машина этого покупателя не найдена"
        )
