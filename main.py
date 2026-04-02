from fastapi import FastAPI
from fastapi import HTTPException
import json

with open("product.json") as file:
    products = json.load(file) 


app = FastAPI()

@app.get("/products")
def get_products():
    return products


@app.get("/products/{product_id}")
def get_product(product_id : int):
    for product in products:
        if product["id"] == product_id:
            return product

    raise HTTPException(status_code=404, detail = "Product not found")