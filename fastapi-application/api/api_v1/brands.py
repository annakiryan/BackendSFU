from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from core.models import db_helper
from core.config import settings
from core.schemas.brand import BrandCreate, BrandRead, BrandUpdate
from core.use_case.brand import brand_service
from core.filters.brand import BrandFilter
from fastapi_pagination import Page
from fastapi_filter import FilterDepends
from api.dependencies.authentication.role_check import get_current_admin_user
from core.exceptions import (
    BrandNotFound,
    BrandAlreadyExists,
)

router = APIRouter(prefix=settings.api.v1.brands, tags=["Brands"])


@router.get(
    "/", response_model=Page[BrandRead],
    dependencies=[Depends(get_current_admin_user)]
)
async def get_all_brands(
    filters: BrandFilter = FilterDepends(BrandFilter),
    db: AsyncSession = Depends(db_helper.session_getter),
):
    try:
        return await brand_service.get_all(db, filters)
    except NotImplementedError as e:
        if "asc_op" in str(e):
            raise HTTPException(
                status_code=400, detail="Сортировка по этому полю невозможна."
            )
        raise e


@router.get(
    "/{brand_id}",
    response_model=BrandRead,
    dependencies=[Depends(get_current_admin_user)],
)
async def get_brand(
    brand_id: int, db: AsyncSession = Depends(db_helper.session_getter)
):
    try:
        return await brand_service.get(db, brand_id)
    except BrandNotFound:
        raise HTTPException(status_code=404, detail="Бренд не найден")


@router.post(
    "/",
    response_model=BrandRead,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(get_current_admin_user)],
)
async def create_brand(
    brand_in: BrandCreate, db: AsyncSession = Depends(db_helper.session_getter)
):
    try:
        return await brand_service.create(db, brand_in)
    except BrandAlreadyExists:
        raise HTTPException(
            status_code=400, detail="Бренд с таким названием уже существует"
        )


@router.put(
    "/{brand_id}",
    response_model=BrandRead,
    dependencies=[Depends(get_current_admin_user)],
)
async def replace_brand(
    brand_id: int,
    brand_in: BrandCreate,
    db: AsyncSession = Depends(db_helper.session_getter),
):
    try:
        return await brand_service.update(db, brand_id, brand_in)
    except BrandAlreadyExists:
        raise HTTPException(
            status_code=400, detail="Бренд с таким названием уже существует"
        )
    except BrandNotFound:
        raise HTTPException(status_code=404, detail="Бренд не найден")


@router.patch(
    "/{brand_id}",
    response_model=BrandRead,
    dependencies=[Depends(get_current_admin_user)],
)
async def update_brand(
    brand_id: int,
    brand_in: BrandUpdate,
    db: AsyncSession = Depends(db_helper.session_getter),
):
    try:
        return await brand_service.update(db, brand_id, brand_in)
    except BrandAlreadyExists:
        raise HTTPException(
            status_code=400, detail="Бренд с таким названием уже существует"
        )
    except BrandNotFound:
        raise HTTPException(status_code=404, detail="Бренд не найден")


@router.delete(
    "/{brand_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(get_current_admin_user)],
)
async def delete_brand(
    brand_id: int, db: AsyncSession = Depends(db_helper.session_getter)
):
    try:
        return await brand_service.delete(db, brand_id)
    except BrandNotFound:
        raise HTTPException(status_code=404, detail="Бренд не найден")
