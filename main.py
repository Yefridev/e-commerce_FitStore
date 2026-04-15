from fastapi import FastAPI
from fastapi import Depends
from fastapi import HTTPException
from pydantic import BaseModel, Field
from database import get_connection


app = FastAPI()


# validar si el producto existe en la base de datos
def product_exists(product_id : int):
    conexion = get_connection()
    cursor = conexion.cursor()

    cursor.execute("SELECT id FROM productos WHERE id = %s", (product_id,))
    result = cursor.fetchone()

    cursor.close()
    conexion.close()

    return result is not None
    

# Modelo
class CartItem(BaseModel):
    product_id : int
    quantity: int = Field(gt=0) #gt=0 significa que la cantidad debe ser mayor a 0

# Carrito de compras en memoria (simulación)
carts: dict [int, list[CartItem]] = {}

#=========================================
#       PRODUCTOS  
#=========================================

# Obtener todos los productos
#--------------------------------
@app.get("/products")
def get_products():
    conexion = get_connection()
    cursor = conexion.cursor(dictionary=True)

    sql = "SELECT * FROM productos"
    cursor.execute(sql)
    products = cursor.fetchall()

    cursor.close()
    conexion.close()

    return products

# Obtener producto por ID
#--------------------------------
@app.get("/products/{product_id}")
def get_product(product_id : int):
    conexion = get_connection()
    cursor = conexion.cursor(dictionary=True)

    cursor.execute("SELECT * FROM productos WHERE id = %s", (product_id,))
    product = cursor.fetchone()

    cursor.close()
    conexion.close()    

    if not product:
        raise HTTPException(status_code=404, detail = "Producto no encontrado")
    return product

# Agregar nuevo producto✅
#--------------------------------
@app.post("/products/")
def add_product(
    nombre: str,
    precio: float,
    descripcion: str,
    stock: int = 0,
    imagen: str = None
):
    conexion = get_connection()
    cursor = conexion.cursor()

    sql = """
    INSERT INTO productos (nombre, precio, descripcion, stock, imagen)
    VALUES (%s,%s,%s,%s,%s)
    """
    cursor.execute(sql, (nombre, precio, descripcion, stock, imagen))
    conexion.commit()

    cursor.close()
    conexion.close()

    return {"message":"Producto creado correctamente"}

# Actualizar producto 
#--------------------------------
@app.put("/products/{product_id}")
def update_product(product_id: int, nombre: str, precio: float):
    if not product_exists(product_id):
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    
    conexion = get_connection()
    cursor = conexion.cursor()

    sql = "UPDATE productos SET nombre=%s, precio=%s WHERE id=%s"
    cursor.execute(sql,(nombre, precio, product_id))
    conexion.commit()

    cursor.close()
    conexion.close()

    return{"message":"Producto actualizado"}

#Eliminar Producto✅
@app.delete("/products/{product_id}")
def delete_product(product_id: int):
    if not product_exists(product_id):
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    
    conexion = get_connection()
    cursor = conexion.cursor()

    cursor.execute("DELETE FROM productos WHERE id = %s",(product_id,))
    conexion.commit()

    cursor.close()
    conexion.close()

    return{"message": "Producto eliminado"}



#=========================================
#---------- CARRITO ----------
#=========================================

# Ver carrito
#--------------------------------
@app.get("/cart/{user_id}")
def get_cart(user_id : int):
    return [item.model_dump() for item in carts.get(user_id, [])]


# Agregar producto al carrito
#--------------------------------
@app.post("/cart/{user_id}")

def add_to_cart(user_id: int, item: CartItem ): #Item será automaticamnete el JSON que envie el usuario
    
    if not product_exists(item.product_id):
        raise HTTPException(status_code=404, detail = "Producto no encontrado")
    
    
    if user_id not in carts:
        carts[user_id] = []
    
    for cart_item in carts[user_id]:
        if cart_item.product_id == item.product_id:
            cart_item.quantity += item.quantity
            return {"message": "Cantidad actualizada"}
        

    carts[user_id].append(item)
    return{"message": "Producto agregado al carrito"}


# Eliminar producto del carrito
#--------------------------------
@app.delete("/cart/{user_id}/{product_id}")
def remove_from_cart(user_id: int, product_id: int):
    if user_id not in carts:
        raise HTTPException(status_code= 404, detail="Carrito no encontrado")
    
    original_len = len(carts[user_id])
    carts[user_id] = [i for i in carts[user_id] if i.product_id != product_id]

    if len(carts[user_id]) == original_len:
        raise HTTPException(status_code=404, detail="producto no encontrado en el carrito")
    
    return{"message": "Producto eliminado del carrito"}