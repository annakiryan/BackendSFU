from fastapi import APIRouter,  HTTPException
from fastapi import Depends
from core.schemas.user import UserRead, UserCreate, UserCreateStaff
from api.dependencies.authentication.role_check import get_current_admin_user
from api.api_v1.fastapi_users import fastapi_users
from api.dependencies.authentication import authentication_backend
from core.config import settings
from core.schemas.user import (
    UserRead,
    UserCreate,
)

router = APIRouter(
    prefix=settings.api.v1.auth,
    tags=["Auth"],
)

# /login
# /logout
router.include_router(
    router=fastapi_users.get_auth_router(
        authentication_backend,
        # requires_verification=True,
    ),
)


# /register
router.include_router(
    router=fastapi_users.get_register_router(
        UserRead,
        UserCreate,
    ),
)

# /staff/register
router.include_router(
    router=fastapi_users.get_register_router(
        UserRead,
        UserCreateStaff,
    ),
    prefix="/staff",
    dependencies=[Depends(get_current_admin_user)],
)


# /request-verify-token
# /verify
router.include_router(
    router=fastapi_users.get_verify_router(UserRead),
)

# /forgot-password
# /reset-password
router.include_router(
    router=fastapi_users.get_reset_password_router(),
)
