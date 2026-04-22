import psycopg2.extras
from fastapi import APIRouter, HTTPException, Depends
from database import get_connection
from schemas.user import UserCreate, UserLogin, Token, UserResponse
from services.auth import hash_password, verify_password, create_access_token
from services.deps import get_current_user

router = APIRouter()

# Registrar usuario
#--------------------------------
@router.post("/users/", response_model=dict, tags=["Usuarios"])
def register_user(user: UserCreate):

    conexion = get_connection()

    if not conexion:
        raise HTTPException(status_code=500, detail="Error de conexión a la base de datos")
    
    try:
        cursor = conexion.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

        #Validar Email unico
        cursor.execute("SELECT id FROM usuarios WHERE email = %s", (user.email,))
        if cursor.fetchone():
            raise HTTPException(status_code=400, detail="El usuario ya existe")

        #hashed password
        hashed = hash_password(user.password)

        cursor.execute(
            "INSERT INTO usuarios (nombre, email, password, rol) VALUES (%s, %s, %s, %s)", 
            (user.nombre, user.email,hashed, "cliente")
        )

        conexion.commit()

    except HTTPException:
        raise
    except Exception as e:
        print("ERROR:",e)
        conexion.rollback()
        raise HTTPException(status_code=400, detail = "Error en registro")

    finally:
        cursor.close()
        conexion.close()

    return{"message": "Usuario registrado correctamente"}

# Cargar un usuario
#--------------------------------
@router.post("/users/login", response_model=Token, tags=["Usuarios"])
def login_user(user: UserLogin):

    conexion = get_connection()
    if not conexion:
        raise HTTPException(status_code=500, detail="Error de conexión a la base de datos")

    try:
        cursor = conexion.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

        cursor.execute("SELECT * FROM usuarios WHERE email = %s", (user.email,))
        db_user = cursor.fetchone()

        cursor.close()

        if not db_user:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")

        if not verify_password(user.password, db_user["password"]):
            raise HTTPException(status_code=401, detail="Contraseña incorrecta")

        token = create_access_token({"user_id": db_user["id"]})
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error en login: {str(e)}")
    finally:
        conexion.close()

    return {
        "access_token": token, "token_type": "bearer"
    }

# Obtener datos del usuario autenticado    
@router.get("/users/me", response_model=UserResponse,  tags=["Usuarios"])
def get_me(current_user: dict = Depends(get_current_user)):
    return {
        "id": current_user["id"],
        "nombre": current_user["nombre"],
        "email": current_user["email"],
        "rol": current_user["rol"]
    }