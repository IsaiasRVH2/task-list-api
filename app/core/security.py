import bcrypt
from jose import jwt
from datetime import datetime, timedelta, timezone
from app.core.config import SECRET_KEY, ALGORITHM, ISS

def get_password_hash(password: str) -> str:
    """Hash a password using bcrypt with a salt."""
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    return hashed_password.decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain password against a hashed password."""
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

def create_access_token(data: dict, expires_delta: int = 3600) -> str:
    payload ={
        "iss": ISS,
        "sub": str(data.get("sub", "")),  # Ensure sub is a string
        "aud": data.get("aud"),
        "iat": datetime.now(timezone.utc), 
        "exp":datetime.now(timezone.utc) + timedelta(minutes=expires_delta) 
        }
    
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    print(f"Created token: {token}")
    return token
    
def verify_access_token(token, aud: str = "tasks") -> dict:
    try:
        print(f"Verifying token: {token}")
        print(f"Using audience: {aud}, issuer: {ISS}")
        print(f"Secret key: {SECRET_KEY}")
        print(f"Algorithm: {ALGORITHM}")
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM], audience=aud, issuer=ISS ) #options = {"verify_exp": True}, audience=aud, issuer=ISS
        if payload.get("exp") < datetime.now(timezone.utc).timestamp():
            raise jwt.JWTError("Token has expired")
        return payload.get("sub", None)
    except jwt.JWTError as e:
        print(f"Token verification error: {e}")
        return None