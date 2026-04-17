from fastapi import APIRouter, HTTPException
from database import get_connection
from schemas.user import UserCreate, UserLogin

router = APIRouter()

# Registrar usuario✅
#--------------------------------
@router.post("/users/")
def register_user(user: UserCreate):

    conexion = get_connection()
    cursor = conexion.cursor()

    # Verifica existencia de email
    cursor.execute("SELECT id FROM usuarios WHERE email = %s", (user.email,))
    existing = cursor.fetchone()

    if existing:
        cursor.close()
        conexion.close()
        raise HTTPException (status_code=400, detail = "El usuario ya existe")
    
    cursor.execute(
        "INSERT INTO usuarios (nombre, email, password) VALUES (%s, %s, %s)", 
        (user.nombre, user.email, user.password)
        )
    conexion.commit()

    cursor.close()
    conexion.close()

    return {"message": "Usuario conectado correctamente"}


# Cargar un usuario
#--------------------------------
@router.post("/user/login")
def login_user(user: UserLogin):

    conexion = get_connection()
    cursor = conexion.cursor(dictionary=True)

    cursor.execute("SELECT * FROM usuarios WHERE email = %s", (user.email,))
    db_user = cursor.fetchone()

    cursor.close()
    conexion.close()

    if not db_user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    if db_user["password"] != user.password:
        raise HTTPException(status_code=401, detail="Contraseña incorrecta")
    
    return{
        "message": "Login exitoso",
        "user_id": db_user["id"],
        "nombre": db_user["nombre"]
        }
        