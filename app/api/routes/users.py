from fastapi import Depends, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.user import UserCreate, UserUpdate, UserResponse
from app.crud.user import create_user, get_user, update_user, deactivate_user
from app.core.database import get_session
from app.core.auth import get_current_user
from app.models.user import User
import app.exceptions as exceptions

router = APIRouter()

@router.post("/users/", response_model=UserResponse)
async def create_user_endpoint(user_create: UserCreate, session: AsyncSession = Depends(get_session)):
    user = await create_user(user_create, session)
    return user

@router.get("/users/me", response_model=UserResponse)
async def get_user_endpoint(session: AsyncSession = Depends(get_session), user: User = Depends(get_current_user)):
    user = await get_user(user.id, session)
    return user

@router.put("/users/me", response_model=UserResponse)
async def update_user_endpoint(user_update: UserUpdate, session: AsyncSession = Depends(get_session), user: User = Depends(get_current_user)):
    user = await update_user(user.id, user_update, session)
    if not user:
        raise exceptions.not_found(message="User update failed.")
    return user

@router.put("/users/deactivate", response_model=dict)
async def deactivate_user_endpoint(session: AsyncSession = Depends(get_session), user: User = Depends(get_current_user)):
    return await deactivate_user(user.id, session)