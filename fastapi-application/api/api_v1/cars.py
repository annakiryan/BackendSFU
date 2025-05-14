from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from core.config import settings
from core.schemas.car import CarCreate, CarUpdate, CarRead
from core.use_case.car import car_service
from core.exceptions import (
    CarNotFound,
    BrandNotFound,
    BrandAlreadyExists,
    BrandRequired,
    OnlyOneWayToCreateBrand,
)
from core.models import db_helper
from core.filters.car import CarFilter
from fastapi_filter import FilterDepends
from fastapi_pagination import Page
from api.dependencies.authentication.role_check import get_current_admin_user

router = APIRouter(prefix=settings.api.v1.cars, tags=["Cars"])


@router.get(
    "/",
    response_model=Page[CarRead],
    dependencies=[Depends(get_current_admin_user)],
)
async def get_all_cars(
    car_filter: CarFilter = FilterDepends(CarFilter),
    db: AsyncSession = Depends(db_helper.session_getter),
):
    try:
        return await car_service.get_all(db, car_filter)
    except NotImplementedError as e:
        if "asc_op" in str(e):
            raise HTTPException(
                status_code=400, detail="Сортировка по этому полю невозможна."
            )
        raise e


@router.get(
    "/{car_id}",
    response_model=CarRead,
    dependencies=[Depends(get_current_admin_user)],
)
async def get_car(car_id: int, db: AsyncSession = Depends(db_helper.session_getter)):
    try:
        return await car_service.get(db, car_id)
    except CarNotFound:
        raise HTTPException(status_code=404, detail="Машина не найдена")


@router.post(
    "/",
    response_model=CarRead,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(get_current_admin_user)],
)
async def create_car(
    car_in: CarCreate, db: AsyncSession = Depends(db_helper.session_getter)
):
    try:
        return await car_service.create(db, car_in)
    except BrandNotFound:
        raise HTTPException(status_code=404, detail="Бренд не найден")
    except BrandAlreadyExists:
        raise HTTPException(
            status_code=400, detail="Бренд с таким названием уже существует"
        )
    except BrandRequired:
        raise HTTPException(
            status_code=400, detail="Нужно указать brand_id или brand_name"
        )
    except OnlyOneWayToCreateBrand:
        raise HTTPException(
            status_code=400,
            detail="Нельзя указывать одновременно и brand_id, и brand_name",
        )


@router.put(
    "/{car_id}",
    response_model=CarRead,
    dependencies=[Depends(get_current_admin_user)],
)
async def replace_car(
    car_id: int, car_in: CarCreate, db: AsyncSession = Depends(db_helper.session_getter)
):
    try:
        return await car_service.update(db, car_id, car_in)
    except CarNotFound:
        raise HTTPException(status_code=404, detail="Машина не найдена")
    except BrandNotFound:
        raise HTTPException(status_code=404, detail="Бренд не найден")
    except BrandAlreadyExists:
        raise HTTPException(
            status_code=400, detail="Бренд с таким названием уже существует"
        )
    except BrandRequired:
        raise HTTPException(
            status_code=400, detail="Нужно указать brand_id или brand_name"
        )
    except OnlyOneWayToCreateBrand:
        raise HTTPException(
            status_code=400,
            detail="Нельзя указывать одновременно и brand_id, и brand_name",
        )


@router.patch(
    "/{car_id}",
    response_model=CarRead,
    dependencies=[Depends(get_current_admin_user)],
)
async def update_car(
    car_id: int, car_in: CarUpdate, db: AsyncSession = Depends(db_helper.session_getter)
):
    try:
        return await car_service.update(db, car_id, car_in)
    except CarNotFound:
        raise HTTPException(status_code=404, detail="Машина не найдена")
    except BrandNotFound:
        raise HTTPException(status_code=404, detail="Бренд не найден")
    except BrandAlreadyExists:
        raise HTTPException(
            status_code=400, detail="Бренд с таким названием уже существует"
        )
    except BrandRequired:
        raise HTTPException(
            status_code=400, detail="Нужно указать brand_id или brand_name"
        )


@router.delete(
    "/{car_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(get_current_admin_user)],
)
async def delete_car(car_id: int, db: AsyncSession = Depends(db_helper.session_getter)):
    try:
        await car_service.delete(db, car_id)
    except CarNotFound:
        raise HTTPException(status_code=404, detail="Машина не найдена")
