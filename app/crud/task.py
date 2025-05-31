from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.task import Task
from app.schemas.task import TaskCreate, TaskUpdate
from app.crud.user import get_user

async def create_task(user_id: int, task_create: TaskCreate, session: AsyncSession):
    task = Task(**task_create.model_dump())
    if user_id is None:
        return {"error": "User ID is required to create a task."}
    user = await get_user(user_id, session)
    if not user or not user.is_active:
        print("Error: User not found.")
        return None
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
        return None
    for field, value in task_update.model_dump(exclude_unset=True).items():
        setattr(task, field, value)
    await session.commit()
    return task

async def delete_task(user_id: int, task_id: int, session: AsyncSession):
    result = await session.execute(select(Task).filter(Task.id == task_id, Task.user_id == user_id))
    task = result.scalars().first()
    if task is None:
        return None
    session.delete(task)
    await session.commit()
    return {"message": "Task deleted successfully."}