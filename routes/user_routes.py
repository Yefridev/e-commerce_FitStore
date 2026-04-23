from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import select
from database import SessionDep
from models.user import Usuario
from schemas.user import UserCreate, UserLogin, Token, UserResponse
from services.auth import hash_password, verify_password, create_access_token
from services.deps import get_current_user

router = APIRouter()

# Registrar usuario
#--------------------------------
@router.post("/users/", response_model=dict, tags=["Usuarios"])
def register_user(user: UserCreate, session: SessionDep):

    existe = session.exec(select(Usuario).where(Usuario.email == user.email)).first()
    if existe:
        raise HTTPException (status_code=400, detail="El usuario ya existe")
    
    nuevo = Usuario(
        nombre=user.nombre,
        email=user.email,
        password= hash_password(user.password),
        rol="cliente"
    )

    session.add(nuevo)
    session.commit()

    return{"message": "Usuario conectado correctamente"}


# Cargar un usuario
#--------------------------------
@router.post("/users/login", response_model=Token, tags=["Usuarios"])
def login_user(user: UserLogin, session: SessionDep):

    db_user = session.exec(select(Usuario).where(Usuario.email == user.email)).first()

    if not db_user:
        raise HTTPException (status_code=404, detail="Usuario no encontrado")
    
    if not verify_password(user.password, db_user.password):
        raise HTTPException(status_code= 401, detail="Contraseña incorrecta")
    
    Token = create_access_token({"user_id": db_user.id})

    return{"access_token": Token, "token_type": "bearer"}



# Obtener datos del usuario autenticado    
@router.get("/users/me", response_model=UserResponse, tags=["Usuarios"])
def get_me(current_user: Usuario = Depends(get_current_user)):
    return {
        "id": current_user["id"],
        "nombre": current_user["nombre"],
        "email": current_user["email"],
        "rol": current_user["rol"]
    }