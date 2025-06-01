from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import or_, and_

from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.core.security import get_password_hash
import app.exceptions as exceptions

async def create_user(user_create: UserCreate, session: AsyncSession):
        if await check_user_email_exists(user_create.email, session):
            raise exceptions.bad_request("User with this email already exists.")
            
        if await check_user_username_exists(user_create.username, session):
            raise exceptions.bad_request("User with this username already exists.")
        
        user = User(
            username=user_create.username,
            email=user_create.email,
            hashed_password=get_password_hash(user_create.password),
            first_name=user_create.first_name,
            last_name=user_create.last_name
        )
        session.add(user)
        await session.commit()
        await session.refresh(user)
        return user

async def get_user(id: int, session: AsyncSession):
    result = await session.execute(select(User).filter(User.id == id, User.is_active == True))
    user = result.scalars().first()
    return user

async def get_user_by_email_or_username(email: str, session: AsyncSession):
    result = await session.execute(select(User).filter(and_(
        or_(User.email == email, User.username == email),
        User.is_active == True
    )))
    user = result.scalars().first()
    return user

async def update_user(id: int, user_update: UserUpdate, session: AsyncSession):
    if user_update.username is not None:
        existing_user = await session.execute(
            select(User).where(User.username == user_update.username)
        )
        existing_user = existing_user.scalars().first()
        if existing_user and existing_user.id != id:
            raise exceptions.bad_request("User with this username already exists.")
    result = await session.execute(select(User).filter(User.id == id, User.is_active == True))
    user = result.scalars().first()
    if not user:
        raise exceptions.not_found(message="User not found.")
    for field, value in user_update.model_dump(exclude_unset=True).items():
        setattr(user, field, value)
    await session.commit()
    return user

async def check_user_email_exists(email: str, session: AsyncSession):
    result = await session.execute(select(User).where(User.email == email))
    return result.scalars().first() is not None
async def check_user_username_exists(username: str, session: AsyncSession):
    result = await session.execute(select(User).where(User.username == username))
    return result.scalars().first() is not None


async def deactivate_user(id: int, session: AsyncSession):
    result = await session.execute(select(User).filter(User.id == id, User.is_active == True))
    user = result.scalars().first()
    if not user:
        raise exceptions.not_found("User not found or already inactive.")
    user.is_active = False
    await session.commit()
    return {"message": "User deactivated successfully."}