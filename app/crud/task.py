from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.task import Task
from app.schemas.task import TaskCreate, TaskUpdate
from app.crud.user import get_user
import app.exceptions as exceptions

async def create_task(user_id: int, task_create: TaskCreate, session: AsyncSession):
    task = Task(**task_create.model_dump())
    user = await get_user(user_id, session)
    if not user or not user.is_active:
        raise exceptions.unprocessable_entity(message="Invalid or inactive user.")
    task.user_id = user_id
    session.add(task)
    await session.commit()
    await session.refresh(task)
    return task

async def get_task(id: int, session: AsyncSession):
    result = await session.execute(select(Task).filter(Task.id == id))
    task = result.scalars().first()
    return task

async def get_tasks_by_user(user_id: int, session: AsyncSession):
    result = await session.execute(select(Task).filter(Task.user_id == user_id))
    tasks = result.scalars().all()
    return tasks

async def update_task(user_id: int, task_id: int, task_update: TaskUpdate, session: AsyncSession):
    result = await session.execute(select(Task).filter(Task.id == task_id, Task.user_id == user_id))
    task = result.scalars().first()
    if not task:
        raise exceptions.not_found(message="Task not found.")
    updates = task_update.model_dump(exclude_unset=True)
    if not updates:
        raise exceptions.bad_request(message="No fields to update.")
    for field, value in updates.items():
        setattr(task, field, value)
    await session.commit()
    return task

async def delete_task(user_id: int, task_id: int, session: AsyncSession):
    result = await session.execute(select(Task).filter(Task.id == task_id, Task.user_id == user_id))
    task = result.scalars().first()
    if task is None:
        raise exceptions.not_found(message="Task not found.")
    session.delete(task)
    await session.commit()
    return {"message": "Task deleted successfully.", "task_id": task_id}