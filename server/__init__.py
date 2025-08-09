from fastapi import FastAPI

from .db import up, migrate
from .routers import (
    user_app,
    task_app,
    project_app
)

app = FastAPI()
app.include_router(user_app)
app.include_router(task_app)
app.include_router(project_app)