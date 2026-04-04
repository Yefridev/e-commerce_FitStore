from fastapi import FastAPI
from fastapi import HTTPException
from pydantic import BaseModel, Field
import json

app = FastAPI()

# Modelo
class CartItem(BaseModel):
    product_id : int
    quantity: int = Field(gt=0) # Me dice quantity debe ser mayor a 0

# Cargar productos desde JSON
with open("product.json") as file:
    products = json.load(file) 


# Obtener producto por ID
def get_product_by_id(product_id : int):
    return next((product for product in products if product["id"] == product_id), None)

carts: dict [int, list[CartItem]] = {}

#---------- PRODUCTOS ----------

# Obtener todos los productos
@app.get("/products")
def get_products():
    return products

# Obtener producto por ID
@app.get("/products/{product_id}")
def get_product(product_id : int):
    product = get_product_by_id(product_id)
    if not product:
        raise HTTPException(status_code=404, detail = "Product not found")
    return product


#---------- CARRITO ----------

# Ver carrito
@app.get("/cart/{user_id}")
def get_cart(user_id : int):
    return [item.model_dump() for item in carts.get(user_id, [])]

# Agregar producto al carrito
@app.post("/cart/{user_id}")
def add_to_cart(user_id: int, item: CartItem ): #Item será automaticamnete el JSON que envie el usuario
    product = get_product_by_id(item.product_id)
    if not product:
        raise HTTPException(status_code=404, detail = "Product not found")
    
    
    if user_id not in carts:
        carts[user_id] = []
    
    for cart_item in carts[user_id]:
        if cart_item.product_id == item.product_id:
            cart_item.quantity += item.quantity
            return {"message": "Cantidad actualizada"}
        

    carts[user_id].append(item)
    return{"message": "Producto agregado al carrito"}

# Eliminar producto del carrito
@app.delete("/cart/{user_id}/{product_id}")
def remove_from_cart(user_id: int, product_id: int):
    if user_id not in carts:
        raise HTTPException(status_code= 404, detail="Carrito no encontrado")
    
    original_len = len(carts[user_id])
    carts[user_id] = [i for i in carts[user_id] if i.product_id != product_id]

    if len(carts[user_id]) == original_len:
        raise HTTPException(status_code=404, detail="producto no encontrado en el carrito")
    
    return{"message": "Producto eliminado del carrito"}