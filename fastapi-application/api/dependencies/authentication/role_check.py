from fastapi import Depends, HTTPException, status
from core.models import User
from api.api_v1.fastapi_users import fastapi_users

get_current_user = fastapi_users.current_user()


async def get_current_admin_user(user: User = Depends(fastapi_users.current_user())):
    if user.role.name != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Только администратор может выполнять это действие",
        )
    return user


async def get_current_employee_or_client_user(
    user: User = Depends(fastapi_users.current_user()),
):
    if user.role not in ("employee", "client"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Только клиент или сотрудник может просматривать заказы",
        )
    return user
