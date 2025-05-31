from fastapi import FastAPI
from app.api.routes import users, tasks, auth


app = FastAPI()

app.include_router(users.router, prefix="/api/users", tags=["Users"])
app.include_router(tasks.router, prefix="/api/tasks", tags=["Tasks"])
app.include_router(auth.router, prefix="/api/auth", tags=["Auth"])