from typing import Optional
from pydantic import BaseModel
from datetime import datetime

class TaskCreate(BaseModel):
    content: str
    is_done: bool = False
    created_at: datetime
    due_date: Optional[datetime] = None
    user_id: int
    
class TaskInDB(TaskCreate):
    id: int

class TaskUpdate(BaseModel):
    content: Optional[str] = None
    is_done: Optional[bool] = None
    due_date: Optional[datetime] = None
    
class TaskResponse(BaseModel):
    content: str
    is_done: bool
    created_at: datetime
    due_date: Optional[datetime] = None
    user_id: int