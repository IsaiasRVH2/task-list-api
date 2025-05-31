from fastapi import Depends, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.schemas.task import TaskCreate, TaskUpdate, TaskResponse
from app.crud.task import create_task, get_tasks_by_user, update_task, delete_task
from app.core.auth import get_current_user
from app.core.database import get_session
from app.models.user import User

router = APIRouter()

@router.post("/tasks/", response_model=TaskResponse)
async def create_task_endpoint(task_create: TaskCreate, session: AsyncSession = Depends(get_session), user: User = Depends(get_current_user)):
    if user is None:
        return {"error": "User not authenticated."}
    task = await create_task(user.id, task_create, session)
    if not task:
        return {"error": "Task creation failed."}
    return task

@router.get("/tasks/", response_model=List[TaskResponse])
async def get_tasks_by_user_endpoint(session: AsyncSession = Depends(get_session), user: User =  Depends(get_current_user)):
    if user is None:
        return {"error": "User not authenticated."}
    user_id = user.id
    if user_id is None:
        return {"error": "User not authenticated."}
    tasks = await get_tasks_by_user(user_id, session)
    if not tasks:
        return {"error": "No tasks found for this user."}
    return tasks

@router.put("/tasks/{task_id}", response_model=TaskResponse)
async def update_task_endpoint(task_id: int, task_update: TaskUpdate, session: AsyncSession = Depends(get_session), user: User = Depends(get_current_user)):
    if user is None:
        return {"error": "User not authenticated."}
    task = await update_task(user.id, task_id, task_update, session)
    if not task:
        return {"error": "Task not found or update failed."}
    return task

@router.delete("/tasks/{task_id}")
async def delete_task_endpoint(task_id: int, session: AsyncSession = Depends(get_session), user: User = Depends(get_current_user)):
    if user is None:
        return {"error": "User not authenticated."}
    result = await delete_task(user.id, task_id, session)
    if not result:
        return {"error": "Task not found or deletion failed."}
    return result