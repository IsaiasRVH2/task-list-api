from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from app.core.config import DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME

db_url = f'postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

Base = declarative_base()
engine = create_engine(db_url)

class AsyncDatabaseSession:
    def __init__(self):
        self._session = None
        self._engine = None
        
    def __getattr__(self, name):
        return getattr(self._session, name)
    
    def init(self):
        self._engine = create_async_engine(db_url, future=True, echo=True)
        self._session = sessionmaker(
            self._engine, expire_on_commit=False, class_=AsyncSession)()
    async def create_all(self):
        self._engine.begin
        
db = AsyncDatabaseSession()
def get_session():
    if not db._session:
        db.init()
    return db._session