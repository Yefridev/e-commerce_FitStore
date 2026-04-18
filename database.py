import mysql.connector

def get_connection():
    try: 
        conexion = mysql.connector.connect(
            host="192.168.1.2",
            port=3306,
            user="root",
            password="",
            database="ecommerce_db",
        )
        if (conexion.is_connected()):
            print("Conexión exitosa a la base de datos")
            return conexion

    except mysql.connector.Error as e:
        print(f"Error al conectar a la base de datos: {e}")
        return None
        