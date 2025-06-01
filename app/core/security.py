import bcrypt
from jose import jwt
from datetime import datetime, timedelta, timezone

import app.exceptions as exceptions
from app.core.config import SECRET_KEY, ALGORITHM, ISS

def get_password_hash(password: str):
    """Hash a password using bcrypt with a salt."""
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    return hashed_password.decode('utf-8')

def verify_password(plain_password: str, hashed_password: str):
    """Verify a plain password against a hashed password."""
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

def create_access_token(data: dict, expires_delta: timedelta = timedelta(minutes=60)) -> str:
    payload ={
        "iss": ISS,
        "sub": str(data.get("sub", "")),  # Ensure sub is a string
        "aud": data.get("aud"),
        "iat": datetime.now(timezone.utc), 
        "exp":datetime.now(timezone.utc) + expires_delta
        }
    
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token
    
def verify_access_token(token, aud: str = "tasks") -> dict:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM], audience=aud, issuer=ISS ) #options = {"verify_exp": True}, audience=aud, issuer=ISS
        return payload.get("sub", None)
    except jwt.ExpiredSignatureError:
        raise exceptions.unauthorized("Token has expired.")
    except jwt.JWTError as e:
        raise exceptions.unauthorized(f"Token verification failed.")