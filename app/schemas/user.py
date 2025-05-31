from datetime import datetime, timezone
from typing import Optional
from pydantic import BaseModel, EmailStr, constr, field_validator
import re

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    first_name: str
    last_name: str
    created_at: datetime = datetime.now(timezone.utc)
    is_active: bool = True
    
    @field_validator("username")
    def validate_username(cls, value: str) -> str:
        if not value.isalnum():
            raise ValueError("Username must be alphanumeric.")
        if len(value) < 3 or len(value) > 20:
            raise ValueError("Username must be between 3 and 20 characters long.")
        return value
    
    @field_validator("password")
    def validate_password(cls, value: str) -> str:
        if len(value) < 8:
            raise ValueError("Password must be at least 8 characters long.")
        if not any(char.isdigit() for char in value):
            raise ValueError("Password must contain at least one digit.")
        if not any(char.isalpha() for char in value):
            raise ValueError("Password must contain at least one letter.")
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", value):
            raise ValueError("La contraseña debe incluir al menos un carácter especial de los siguientes: [!@#$%^&*(),.?\":{}|<>]")
        return value
    

class UserInDB(UserCreate):
    id: int
    
class UserUpdate(BaseModel):
    username: Optional[str] = None
    password: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    is_active: Optional[bool] = None
    @field_validator("username")
    def validate_username(cls, value: str) -> str:
        if not value.isalnum():
            raise ValueError("Username must be alphanumeric.")
        if len(value) < 3 or len(value) > 20:
            raise ValueError("Username must be between 3 and 20 characters long.")
        return value
    
    @field_validator("password")
    def validate_password(cls, value: str) -> str:
        if len(value) < 8:
            raise ValueError("Password must be at least 8 characters long.")
        if not re.search(r"[A-Z]", value):
            raise ValueError("La contraseña debe incluir al menos una letra mayúscula")
        if not re.search(r"[a-z]", value):
            raise ValueError("La contraseña debe incluir al menos una letra minúscula")
        if not re.search(r"\d", value):
            raise ValueError("La contraseña debe incluir al menos un número")
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", value):
            raise ValueError("La contraseña debe incluir al menos un carácter especial de los siguientes: [!@#$%^&*(),.?\":{}|<>]")
        return value

class UserResponse(BaseModel):
    username: str
    email: str
    first_name: str
    last_name: str
    created_at: datetime
    is_active: bool