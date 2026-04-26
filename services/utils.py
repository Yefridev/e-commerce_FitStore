from database import get_connection


def existe_producto(producto_id: int):
    conexion = get_connection()
    cursor = conexion.cursor()

    cursor.execute("SELECT id FROM productos WHERE id = %s", (producto_id,))
    resultado = cursor.fetchone()

    cursor.close()
    conexion.close()

    return resultado is not None