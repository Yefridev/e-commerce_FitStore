from fastapi import FastAPI
from routes.user_routes import router as user_router
from routes.product_routes import router as product_router
from routes.cart_routes import router as cart_router


app = FastAPI()

app.include_router(user_router)
app.include_router(product_router)
app.include_router(cart_router)