from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from app.crud.user import get_user_by_email_or_username
from app.core.auth import get_current_user
from app.core.database import get_session
from app.core.security import verify_password, create_access_token
from app.models.user import User
from app.schemas.token import Token
from app.schemas.user import UserResponse

router = APIRouter()
@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), session=Depends(get_session)):
    email_username = form_data.username
    password = form_data.password
    user = await get_user_by_email_or_username(email_username, session)
    if user is None:
        return {"error": "Invalid credentials"}
    if not verify_password(password, user.hashed_password):
        return {"error": "Invalid credentials"}
    access_token = create_access_token(data={"sub": user.id, "aud": "tasks"})
    return Token(access_token=access_token, token_type="bearer")

@router.get("/user", response_model=UserResponse)
def read_users_me(current_user: User = Depends(get_current_user)):
    if current_user is None:
        return {"error": "Not authenticated"}
    return current_user