from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import timedelta

from app.core.security import create_access_token, verify_password, verify_access_token
from app.crud.user import get_user_by_email_or_username, get_user
from app.core.config import ACCESS_TOKEN_EXPIRE_MINUTES
from app.core.database import get_session
from app.models.user import User
import app.exceptions as exceptions

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/login")

async def authenticate_user(email_username: str, password: str, session: AsyncSession):
    user = await get_user_by_email_or_username(email_username, session)
    if user is None:
        raise exceptions.UserNotFoundException("User not found")
    if not verify_password(password, user.hashed_password):
        raise exceptions.unauthorized("User authentication failed.")
    return user

def generate_token(user: User):
    return create_access_token(data={"sub": user.id}, expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))

async def get_current_user(token: str = Depends(oauth2_scheme), session: AsyncSession = Depends(get_session)):
    user_id = int(verify_access_token(token))
    if user_id is None:
        raise exceptions.unauthorized(message="User authentication failed.")
    user = await get_user(user_id, session)
    if user is None:
        raise exceptions.unauthorized(message="User authentication failed.")
    return user
    