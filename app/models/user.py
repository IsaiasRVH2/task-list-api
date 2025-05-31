from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.dialects.postgresql import TIMESTAMP
from sqlalchemy.sql import func
from datetime import datetime, timezone
from app.models.base import Base

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),default=func.now())
    is_active = Column(Boolean, default=True, nullable=False)
    
