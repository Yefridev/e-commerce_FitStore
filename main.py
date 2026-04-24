from fastapi import FastAPI
from contextlib import asynccontextmanager
from database import create_db_and_tables
from routes.user_routes import router as user_router
from routes.category_routes import router as category_router
import models.user


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()  # crea las tablas al arrancar
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(user_router)
app.include_router(category_router)