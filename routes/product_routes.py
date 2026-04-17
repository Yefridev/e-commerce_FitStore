from fastapi import APIRouter, HTTPException
from database import get_connection
from services.utils import product_exists
from schemas.product import ProductCreate, ProductUpdate

router = APIRouter()

# Obtener todos los productos✅
#--------------------------------
@router.get("/products")
def get_products():

    conexion = get_connection()
    cursor = conexion.cursor(dictionary=True)

    sql = "SELECT * FROM productos"
    cursor.execute(sql)
    products = cursor.fetchall()

    cursor.close()
    conexion.close()

    return products

# Obtener producto por ID✅
#--------------------------------
@router.get("/products/{product_id}")
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
@router.post("/products/")
def add_product(product: ProductCreate):
    conexion = get_connection()
    cursor = conexion.cursor()

    cursor.execute(
        "INSERT INTO productos (nombre, precio, descripcion, stock, imagen) VALUES (%s, %s, %s, %s, %s)",
        (product.nombre, product.precio, product.descripcion, product.stock, product.imagen)
    )
    conexion.commit()

    cursor.close()
    conexion.close()

    return {"message": "Producto creado correctamente"}

# Actualizar producto✅
@router.put("/products/{product_id}")
def update_product(product_id: int, product: ProductUpdate):
    if not product_exists(product_id):
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    
    conexion = get_connection()
    cursor = conexion.cursor()

    cursor.execute(
        "UPDATE productos SET nombre = %s, precio = %s, descripcion = %s, stock = %s, imagen = %s WHERE id = %s",
        (product.nombre, product.precio, product.descripcion, product.stock, product.imagen, product_id)
    )
    conexion.commit()

    cursor.close()
    conexion.close()

    return {"message": "Producto actualizado correctamente"}

# Eliminar producto✅
@router.delete("/products/{product_id}")
def delete_product(product_id: int):
    if not product_exists(product_id):
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    conexion = get_connection()
    cursor = conexion.cursor()

    cursor.execute("DELETE FROM productos WHERE id = %s", (product_id,))
    conexion.commit()

    cursor.close()
    conexion.close()

    return {"message": "Producto eliminado correctamente"}

