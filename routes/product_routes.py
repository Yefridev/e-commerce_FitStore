from fastapi import APIRouter, HTTPException
from database import get_connection
from services.utils import product_exists
from schemas.product import ProductCreate, ProductUpdate

router = APIRouter()

# Obtener todos los productos✅
#--------------------------------
@router.get("/products", tags=["Productos"])
def get_products():

    conexion = get_connection()
    if not conexion:
        raise HTTPException(status_code=500, detail="Error de conexión a la base de datos")
    
    cursor = conexion.cursor(dictionary=True)

    sql = "SELECT * FROM productos"
    cursor.execute(sql)
    products = cursor.fetchall()

    cursor.close()
    conexion.close()

    return products

# Obtener producto por ID✅
#--------------------------------
@router.get("/products/{product_id}", tags=["Productos"])
def get_product(product_id : int):

    conexion = get_connection()
    if not conexion:
        raise HTTPException(status_code=500, detail="Error de conexión a la base de datos")
    
    cursor = conexion.cursor(dictionary=True)

    cursor.execute("SELECT * FROM productos WHERE id = %s", (product_id,))
    product = cursor.fetchone()

    cursor.close()
    conexion.close()    

    if not product:
        raise HTTPException(status_code=404, detail = "Producto no encontrado")
    return product

# Agregar nuevo producto✅
@router.post("/products/", tags=["Productos"])
def add_product(product: ProductCreate):
    conexion = get_connection()
    if not conexion:
        raise HTTPException(status_code=500, detail="Error de conexión a la base de datos")
    
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
@router.put("/products/{product_id}", tags=["Productos"])
def update_product(product_id: int, product: ProductUpdate):
    if not product_exists(product_id):
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    
    conexion = get_connection()
    if not conexion:
        raise HTTPException(status_code=500, detail="Error de conexión a la base de datos")
    
    cursor = conexion.cursor()

    updates = []
    values = []
    
    if product.nombre is not None:
        updates.append("nombre = %s")
        values.append(product.nombre)
    if product.precio is not None:
        updates.append("precio = %s")
        values.append(product.precio)
    if product.descripcion is not None:
        updates.append("descripcion = %s")
        values.append(product.descripcion)
    if product.stock is not None:
        updates.append("stock = %s")
        values.append(product.stock)
    if product.imagen is not None:
        updates.append("imagen = %s")
        values.append(product.imagen)
    
    if not updates:
        raise HTTPException(status_code=400, detail="No hay campos para actualizar")
    
    values.append(product_id)
    
    sql = f"UPDATE productos SET {', '.join(updates)} WHERE id = %s"
    cursor.execute(sql, tuple(values))
    conexion.commit()

    cursor.close()
    conexion.close()

    return {"message": "Producto actualizado correctamente"}

# Eliminar producto✅
@router.delete("/products/{product_id}", tags=["Productos"])
def delete_product(product_id: int):
    if not product_exists(product_id):
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    conexion = get_connection()
    if not conexion:
        raise HTTPException(status_code=500, detail="Error de conexión a la base de datos")
    
    cursor = conexion.cursor()

    cursor.execute("DELETE FROM productos WHERE id = %s", (product_id,))
    conexion.commit()

    cursor.close()
    conexion.close()

    return {"message": "Producto eliminado correctamente"}

