from app.core.security import create_access_token, verify_password
from app.crud.user import get_user_by_email_or_username
from app.core.config import ACCESS_TOKEN_EXPIRE_MINUTES
from app.models.user import User

async def authenticate_user(email_username: str, password: str) -> User | None:
    user = await get_user_by_email_or_username(email_username)
    if user is None:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user

def generate_token(user: User, aud: str):
    return create_access_token(data={"sub": user.id, "aud":aud}, expires_delta=ACCESS_TOKEN_EXPIRE_MINUTES)