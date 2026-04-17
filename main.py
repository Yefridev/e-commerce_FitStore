from fastapi import FastAPI
from routes import user_routes, product_routes, cart_routes


app = FastAPI()

app.include_router(user_router)
app.include_router(product_router)
app.include_router(cart_router)