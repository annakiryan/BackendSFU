from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer

from core.config import settings

from .auth import router as auth_router
from .users import router as users_router
from .brands import router as brands_router
from .cars import router as cars_router
from .customer_cars import router as customer_cars_router
from .orders import router as orders_router
from .services import router as services_router

http_bearer = HTTPBearer(auto_error=False)

router = APIRouter(
    prefix=settings.api.v1.prefix,
    dependencies=[Depends(http_bearer)],
)
router.include_router(auth_router)
router.include_router(users_router)
router.include_router(brands_router)
router.include_router(cars_router)
router.include_router(customer_cars_router)
router.include_router(orders_router)
router.include_router(services_router)
