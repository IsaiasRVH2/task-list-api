from fastapi import Depends, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.user import UserCreate, UserUpdate, UserResponse
from app.crud.user import create_user, get_user, get_user_by_email_or_username, update_user
from app.core.database import get_session

router = APIRouter()

@router.post("/users/", response_model=UserResponse)
async def create_user_endpoint(user_create: UserCreate, session: AsyncSession = Depends(get_session)):
    user = await create_user(user_create, session)
    if not user:
        return {"error": "User creation failed or user already exists."}
    return user

@router.get("/users/{user_id}", response_model=UserResponse)
async def get_user_endpoint(user_id: int, session: AsyncSession = Depends(get_session)):
    user = await get_user(user_id, session)
    if not user:
        return {"error": "User not found."}
    return user

@router.put("/users/{user_id}", response_model=UserResponse)
async def update_user_endpoint(user_id: int, user_update: UserUpdate, session: AsyncSession = Depends(get_session)):
    user = await update_user(user_id, user_update, session)
    if not user:
        return {"error": "User not found or update failed."}
    return user