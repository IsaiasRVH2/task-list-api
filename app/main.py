from fastapi import FastAPI
from app.api.routes import users, tasks, auth


app = FastAPI()

app.include_router(users.router, prefix="/api", tags=["Users"])
app.include_router(tasks.router, prefix="/api", tags=["Tasks"])
app.include_router(auth.router, prefix="/api", tags=["Auth"])