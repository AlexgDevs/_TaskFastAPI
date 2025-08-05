from fastapi import FastAPI

from .db import up, migrate

app = FastAPI()