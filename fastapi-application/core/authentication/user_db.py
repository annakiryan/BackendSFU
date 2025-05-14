from fastapi_users.db import SQLAlchemyUserDatabase
from sqlalchemy.orm import selectinload
from core.models import User
from sqlalchemy import select


class CustomUserDatabase(SQLAlchemyUserDatabase):
    async def create(self, create_dict: dict) -> User:
        user = await super().create(create_dict)
        stmt = (
            select(User)
            .options(selectinload(User.role))
            .where(User.id == user.id)
        )
        result = await self.session.execute(stmt)
        return result.scalar_one()

    async def get(self, id: int) -> User | None:
        query = select(User).options(selectinload(User.role)).filter(User.id == id)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()
