from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from core.config import settings
from core.schemas.order import OrderCreate, OrderRead, OrderAddServices
from core.schemas.service import ServiceRead
from core.use_case.order import order_service
from core.exceptions import (
    OrderNotFound,
    OrderCompleted,
    ServiceNotFound,
    ServicesAlreadyAdded,
    PermissionDenied,
)
from core.models import db_helper, User
from core.filters.order import OrderFilter
from fastapi_filter import FilterDepends
from fastapi_pagination import Page
from api.dependencies.authentication.role_check import (
    get_current_admin_user,
    get_current_user,
)

router = APIRouter(prefix=settings.api.v1.orders, tags=["Orders"])


@router.get("/", response_model=Page[OrderRead])
async def get_all_orders(
    order_filter: OrderFilter = FilterDepends(OrderFilter),
    db: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(get_current_user),
):
    try:
        return await order_service.get_all(db, order_filter, user)
    except PermissionDenied:
        raise HTTPException(status_code=403, detail="Доступ запрещен")
    except NotImplementedError as e:
        if "asc_op" in str(e):
            raise HTTPException(
                status_code=400, detail="Сортировка по этому полю невозможна."
            )
        raise e


@router.get("/{order_id}", response_model=OrderRead)
async def get_order(
    order_id: int,
    db: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(get_current_user),
):
    try:
        return await order_service.get_my_order(db, order_id, user)
    except OrderNotFound:
        raise HTTPException(status_code=404, detail="Заказ не найден")
    except PermissionDenied:
        raise HTTPException(status_code=403, detail="Доступ запрещен")


@router.get("/{order_id}/services", response_model=Page[ServiceRead])
async def get_order_services(
    order_id: int,
    db: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(get_current_user),
):
    try:
        return await order_service.get_order_services(db, order_id, user)
    except OrderNotFound:
        raise HTTPException(status_code=404, detail="Заказ не найден")
    except PermissionDenied:
        raise HTTPException(status_code=403, detail="Доступ запрещен")


@router.post(
    "/",
    response_model=OrderRead,
    status_code=status.HTTP_201_CREATED,
)
async def create_order(
    order_in: OrderCreate,
    db: AsyncSession = Depends(db_helper.session_getter),
    admin: User = Depends(get_current_admin_user),
):
    return await order_service.create(db, order_in, admin.id)


# @router.put("/{order_id}", response_model=OrderRead)
# async def replace_order(
#     order_id: int,
#     order_in: OrderCreate,
#     db: AsyncSession = Depends(db_helper.session_getter),
# ):
#     try:
#         return await order_service.update(db, order_id, order_in)
#     except OrderNotFound:
#         raise HTTPException(status_code=404, detail="Заказ не найден")
#     except OrderCompleted:
#         raise HTTPException(
#             status_code=400,
#             detail="Вы не можете редактировать заказ, так как он уже выполнен",
#         )
#     except ServicesAlreadyAdded:
#         raise HTTPException(
#             status_code=400, detail="Все выбранные услуги уже добавлены в заказ"
#         )
#     except ServiceNotFound:
#         raise HTTPException(
#             status_code=404, detail="Выбранные услуги не найдены"
#         )


@router.patch(
    "/{order_id}",
    response_model=OrderRead,
    dependencies=[Depends(get_current_admin_user)],
)
async def update_order(
    order_id: int,
    order_in: OrderAddServices,
    db: AsyncSession = Depends(db_helper.session_getter),
):
    try:
        return await order_service.update(db, order_id, order_in)
    except OrderNotFound:
        raise HTTPException(status_code=404, detail="Заказ не найден")
    except OrderCompleted:
        raise HTTPException(
            status_code=400,
            detail="Вы не можете редактировать заказ, так как он уже выполнен",
        )
    except ServicesAlreadyAdded as e:
        raise e
    except ServiceNotFound:
        raise HTTPException(status_code=404, detail="Выбранные услуги не найдены")


@router.patch(
    "/{order_id}/complete",
    response_model=OrderRead,
    dependencies=[Depends(get_current_admin_user)],
)
async def complete_order(
    order_id: int,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(db_helper.session_getter),
):
    return await order_service.update_status(db, order_id, background_tasks)


@router.delete(
    "/{order_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(get_current_admin_user)],
)
async def delete_order(
    order_id: int, db: AsyncSession = Depends(db_helper.session_getter)
):
    try:
        await order_service.delete(db, order_id)
    except OrderNotFound:
        raise HTTPException(status_code=404, detail="Заказ не найден")
