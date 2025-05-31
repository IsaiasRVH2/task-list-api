from fastapi import APIRouter, Depends
from app.crud.user import get_user_by_email_or_username
from app.core.database import get_session
from app.core.security import verify_password, create_access_token
from app.schemas.token import Token

router = APIRouter()
@router.post("/login", response_model=Token)
async def login(email_username: str, password: str, session=Depends(get_session)):
    user = await get_user_by_email_or_username(email_username, session)
    if user is None:
        return {"error": "Invalid credentials"}
    if not verify_password(password, user.hashed_password):
        return {"error": "Invalid credentials"}
    access_token = create_access_token(data={"sub": user.id, "aud": "tasks"})
    return Token(access_token=access_token, token_type="bearer")
    