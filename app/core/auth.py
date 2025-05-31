from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import create_access_token, verify_password, verify_access_token
from app.crud.user import get_user_by_email_or_username, get_user
from app.core.config import ACCESS_TOKEN_EXPIRE_MINUTES
from app.core.database import get_session
from app.models.user import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/login")

async def authenticate_user(email_username: str, password: str) -> User | None:
    user = await get_user_by_email_or_username(email_username)
    if user is None:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user

def generate_token(user: User, aud: str):
    return create_access_token(data={"sub": user.id, "aud":aud}, expires_delta=ACCESS_TOKEN_EXPIRE_MINUTES)

async def get_current_user(aud: str, token: str = Depends(oauth2_scheme), session: AsyncSession = Depends(get_session)) -> User | None:
    try:
        user_id = int(verify_access_token(token, aud))
        if user_id is None:
            return None
        user = await get_user(user_id, session)
        if user is None:
            return None
        return user
    except Exception as e:
        print(f"Error verifying token: {e}")
        return None