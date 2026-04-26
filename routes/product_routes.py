from fastapi import APIRouter, HTTPException
from database import get_connection
from services.utils import existe_producto
from schemas.product import ProductoCrear, ProductoActualizar

router = APIRouter()

# Obtener todos los productos
@router.get("/productos", tags=["Productos"])
def obtener_productos():

    conexion = get_connection()
    if not conexion:
        raise HTTPException(status_code=500, detail="Error de conexión a la base de datos")
    
    cursor = conexion.cursor(dictionary=True)

    sql = "SELECT * FROM productos"
    cursor.execute(sql)
    productos = cursor.fetchall()

    cursor.close()
    conexion.close()

    return productos

# Obtener producto por ID
@router.get("/productos/{producto_id}", tags=["Productos"])
def obtener_producto(producto_id: int):

    conexion = get_connection()
    if not conexion:
        raise HTTPException(status_code=500, detail="Error de conexión a la base de datos")
    
    cursor = conexion.cursor(dictionary=True)

    cursor.execute("SELECT * FROM productos WHERE id = %s", (producto_id,))
    producto = cursor.fetchone()

    cursor.close()
    conexion.close()    

    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return producto

# Agregar nuevo producto
@router.post("/productos/", tags=["Productos"])
def agregar_producto(producto: ProductoCrear):
    conexion = get_connection()
    if not conexion:
        raise HTTPException(status_code=500, detail="Error de conexión a la base de datos")
    
    cursor = conexion.cursor()

    cursor.execute(
        "INSERT INTO productos (nombre, precio, descripcion, stock, imagen) VALUES (%s, %s, %s, %s, %s)",
        (producto.nombre, producto.precio, producto.descripcion, producto.stock, producto.imagen)
    )
    conexion.commit()

    cursor.close()
    conexion.close()

    return {"message": "Producto creado correctamente"}

# Actualizar producto
@router.put("/productos/{producto_id}", tags=["Productos"])
def actualizar_producto(producto_id: int, producto: ProductoActualizar):
    if not existe_producto(producto_id):
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    
    conexion = get_connection()
    if not conexion:
        raise HTTPException(status_code=500, detail="Error de conexión a la base de datos")
    
    cursor = conexion.cursor()

    actualizaciones = []
    valores = []
    
    if producto.nombre is not None:
        actualizaciones.append("nombre = %s")
        valores.append(producto.nombre)
    if producto.precio is not None:
        actualizaciones.append("precio = %s")
        valores.append(producto.precio)
    if producto.descripcion is not None:
        actualizaciones.append("descripcion = %s")
        valores.append(producto.descripcion)
    if producto.stock is not None:
        actualizaciones.append("stock = %s")
        valores.append(producto.stock)
    if producto.imagen is not None:
        actualizaciones.append("imagen = %s")
        valores.append(producto.imagen)
    
    if not actualizaciones:
        raise HTTPException(status_code=400, detail="No hay campos para actualizar")
    
    valores.append(producto_id)
    
    sql = f"UPDATE productos SET {', '.join(actualizaciones)} WHERE id = %s"
    cursor.execute(sql, tuple(valores))
    conexion.commit()

    cursor.close()
    conexion.close()

    return {"message": "Producto actualizado correctamente"}

# Eliminar producto
@router.delete("/productos/{producto_id}", tags=["Productos"])
def eliminar_producto(producto_id: int):
    if not existe_producto(producto_id):
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    conexion = get_connection()
    if not conexion:
        raise HTTPException(status_code=500, detail="Error de conexión a la base de datos")
    
    cursor = conexion.cursor()

    cursor.execute("DELETE FROM productos WHERE id = %s", (producto_id,))
    conexion.commit()

    cursor.close()
    conexion.close()

    return {"message": "Producto eliminado correctamente"}