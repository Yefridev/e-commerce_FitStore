from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from database import create_db_and_tables
from routes.user_routes import router as user_router
from routes.category_routes import router as category_router
from routes.product_routes import router as product_router
from routes.cart_routes import router as cart_router
from routes.target_routes import router as target_router
from routes. address_routes import router as address_router
from routes.order_routes import router as order_router
import models.user
import models.category
import models.product
import models.cart
import models.address
import models.order


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan)

# CORS primero — siempre antes de los routers
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers después
app.include_router(user_router)
app.include_router(category_router)
app.include_router(product_router)
app.include_router(cart_router)
app.include_router(address_router)
app.include_router(order_router)
app.include_router(target_router)

# Servir frontend estático
app.mount("/static", StaticFiles(directory="frontend"), name="static")

# Redirigir raíz al frontend
@app.get("/")
async def root():
    return RedirectResponse(url="/static/index.html")