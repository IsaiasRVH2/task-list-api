from fastapi import Depends, APIRouter, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.schemas.task import TaskCreate, TaskUpdate, TaskResponse
from app.crud.task import create_task, get_tasks_by_user, update_task, delete_task
from app.core.auth import get_current_user
from app.core.database import get_session
from app.models.user import User
import app.exceptions as exceptions

router = APIRouter()

@router.post("/tasks/", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task_endpoint(task_create: TaskCreate, session: AsyncSession = Depends(get_session), user: User = Depends(get_current_user)):
    task = await create_task(user.id, task_create, session)
    if not task:
        raise exceptions.bad_request(message="Task creation failed.")
    return task

@router.get("/tasks/", response_model=List[TaskResponse])
async def get_tasks_by_user_endpoint(session: AsyncSession = Depends(get_session), user: User =  Depends(get_current_user)):
    user_id = user.id
    tasks = await get_tasks_by_user(user_id, session)
    return tasks

@router.put("/tasks/{task_id}", response_model=TaskResponse)
async def update_task_endpoint(task_id: int, task_update: TaskUpdate, session: AsyncSession = Depends(get_session), user: User = Depends(get_current_user)):
    task = await update_task(user.id, task_id, task_update, session)
    if not task:
        raise exceptions.not_found(message="Task not found or update failed.")
    return task

@router.delete("/tasks/{task_id}", response_model=dict)
async def delete_task_endpoint(task_id: int, session: AsyncSession = Depends(get_session), user: User = Depends(get_current_user)):
    result = await delete_task(user.id, task_id, session)
    if not result:
        raise exceptions.not_found(message="Task not found or deletion failed.")
    return result