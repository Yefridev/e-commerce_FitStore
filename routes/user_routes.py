from fastapi import APIRouter, HTTPException
from fastapi import Depends
from database import get_connection
from schemas.user import UserCreate, UserLogin, Token, UserResponse
from services.auth import hash_password, verify_password, create_access_token
from services.deps import get_current_user

router = APIRouter()

# Registrar usuario
#--------------------------------
@router.post("/users/", response_model=dict)
def register_user(user: UserCreate):

    if len(user.password.encode('utf-8')) > 72:
        raise HTTPException(status_code=400, detail="La contraseña es muy larga (máximo 72 caracteres)")
    
    conexion = get_connection()
    if not conexion:
        raise HTTPException(status_code=500, detail="Error de conexión a la base de datos")
    
    cursor = conexion.cursor()

    cursor.execute("SELECT id FROM usuarios WHERE email = %s", (user.email,))
    if cursor.fetchone():
        cursor.close()
        conexion.close()
        raise HTTPException (status_code=400, detail = "El usuario ya existe")
    
    hashed_password = hash_password(user.password)

    cursor.execute(
        "INSERT INTO usuarios (nombre, email, password, rol) VALUES (%s, %s, %s, %s)", 
        (user.nombre, user.email, hashed_password, user.rol)
        )
    conexion.commit()

    cursor.close()
    conexion.close()

    return {"message": "Usuario registrado correctamente"}


# Cargar un usuario
#--------------------------------
@router.post("/users/login", response_model=Token)
def login_user(user: UserLogin):

    conexion = get_connection()
    if not conexion:
        raise HTTPException(status_code=500, detail="Error de conexión a la base de datos")
    
    cursor = conexion.cursor(dictionary=True)

    cursor.execute("SELECT * FROM usuarios WHERE email = %s", (user.email,))
    db_user = cursor.fetchone()

    cursor.close()
    conexion.close()

    if not db_user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    if not verify_password(user.password, db_user["password"]):
        raise HTTPException(status_code=401, detail="Contraseña incorrecta")
    
    token = create_access_token({"user_id": db_user["id"]})
    
    return{
        "access_token": token,
        "token_type": "bearer"
        }

# Obtener datos del usuario autenticado    
@router.get("/users/me", response_model=UserResponse)
def get_me(current_user: dict = Depends(get_current_user)):
    return {
        "id": current_user["id"],
        "nombre": current_user["nombre"],
        "email": current_user["email"],
        "rol": current_user["rol"]
    }