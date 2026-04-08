import sqlite3

connection = sqlite3.connect("ecommerce.db")
cursor = connection.cursor()# Crear un cursor para ejecutar comandos SQL

# Crear la tabla de productos si no existe
cursor.execute("""
    CREATE TABLE IF NOT EXISTS products(
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        size TEXT NOT NULL,
        price REAL NOT NULL,
        stock INTEGER NOT NULL
    )
""")
# Insertar un producto de ejemplo
cursor.execute("""         
    INSERT INTO products (name, size, price, stock) VALUES (?,?,?,?)""",
    ("Camiseta Slim", "L", 75000, 10)
)

# Ejecutar una consulta para obtener un producto por su nombre
cursor.execute("SELECT * FROM products WHERE name = ?", 
    ("Camiseta Slim",)
)
result = cursor.fetchone()


products = cursor.fetchall() #Obtener todos los productos de la base de datos
print(products)

connection.commit() #Guardar los cambios en la base de datos