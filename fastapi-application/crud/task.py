from sqlalchemy.ext.asyncio import AsyncSession
from typing import Sequence, Optional
from sqlalchemy import select
from core.models.tasks import Task
from core.schemas.task import TaskCreate, TaskReplace, TaskComplete


async def get_all_tasks(session: AsyncSession) -> Sequence[Task]:
    stmt = select(Task).order_by(Task.id)
    result = await session.scalars(stmt)
    return result.all()


async def get_task_by_id(session: AsyncSession, task_id: int) -> Optional[Task]:
    stmt = select(Task).where(Task.id == task_id)
    result = await session.execute(stmt)
    return result.scalar_one_or_none()


async def create_task(session: AsyncSession, task_in: TaskCreate) -> Optional[Task]:
    task = Task(**task_in.model_dump())
    session.add(task)
    await session.commit()
    await session.refresh(task)
    return task


async def update_task(
    session: AsyncSession, task_id: int, task_in: TaskReplace
) -> Optional[Task]:
    db_task = await get_task_by_id(session, task_id)
    if not db_task:
        return None
    for field, value in task_in.model_dump(exclude_unset=True).items():
        setattr(db_task, field, value)
    await session.commit()
    await session.refresh(db_task)
    return db_task


async def complete_task(
    session: AsyncSession, task_id: int, task_in: TaskComplete
) -> Optional[Task]:
    db_task = await get_task_by_id(session, task_id)
    if not db_task:
        return None
    db_task.is_completed = task_in.is_completed
    await session.commit()
    await session.refresh(db_task)
    return db_task


async def delete_task(session: AsyncSession, task_id: int) -> Optional[Task]:
    db_task = await get_task_by_id(session, task_id)
    if not db_task:
        return None
    await session.delete(db_task)
    await session.commit()
    return db_task
