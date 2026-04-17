from database import get_connection

# validar si el producto existe en la base de datos
def product_exists(product_id : int):
    conexion = get_connection()
    cursor = conexion.cursor()

    cursor.execute("SELECT id FROM productos WHERE id = %s", (product_id,))
    result = cursor.fetchone()

    cursor.close()
    conexion.close()

    return result is not None
    