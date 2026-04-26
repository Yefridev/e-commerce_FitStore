from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import select
from database import SessionDep
from models.user import Usuario
from schemas.user import UsuarioCrear, UsuarioLogin, Token, UsuarioRespuesta
from services.auth import crear_hash_password, verificar_password, crear_token_acceso
from services.deps import obtener_usuario_actual, requerir_admin

router = APIRouter()

# Registrar nuevo usuario
@router.post("/usuarios/", response_model=dict, tags=["Usuarios"])
def registrar_usuario(usuario: UsuarioCrear, session: SessionDep):

    existe = session.exec(select(Usuario).where(Usuario.email == usuario.email)).first()
    if existe:
        raise HTTPException (status_code=400, detail="El usuario ya existe")
    
    nuevo = Usuario(
        nombre=usuario.nombre,
        email=usuario.email,
        password= crear_hash_password(usuario.password),
        rol="cliente"
    )

    session.add(nuevo)
    session.commit()

    return{"message": "Usuario conectado correctamente"}

# Iniciar sesión y obtener token
@router.post("/usuarios/login", response_model=Token, tags=["Usuarios"])
def iniciar_sesion(usuario: UsuarioLogin, session: SessionDep):

    db_usuario = session.exec(select(Usuario).where(Usuario.email == usuario.email)).first()

    if not db_usuario:
        raise HTTPException (status_code=404, detail="Usuario no encontrado")
    
    if not verificar_password(usuario.password, db_usuario.password):
        raise HTTPException(status_code= 401, detail="Contraseña incorrecta")
    
    Token = crear_token_acceso({"usuario_id": db_usuario.id})

    return{"access_token": Token, "token_type": "bearer"}

# Crear un nuevo admin
@router.post("/usuarios/crear-admin", response_model=dict, tags=["Usuarios"])
def crear_admin(usuario: UsuarioCrear, session: SessionDep, _: Usuario = Depends(requerir_admin)):

    existe = session.exec(select(Usuario).where(Usuario.email == usuario.email)).first()
    if existe:
        raise HTTPException (status_code=400, detail="El usuario ya existe")
    
    nuevo = Usuario(
        nombre=usuario.nombre,
        email=usuario.email,
        password=crear_hash_password(usuario.password),
        rol="admin"
    )

    session.add(nuevo)
    session.commit()

    return{"message": "Admin creado correctamente"}

# Obtener mi perfil
@router.get("/usuarios/mi-perfil", response_model=UsuarioRespuesta, tags=["Usuarios"])
def obtener_mi_perfil(usuario_actual: Usuario = Depends(obtener_usuario_actual)):
    return {
        "id": usuario_actual.id,
        "nombre": usuario_actual.nombre,
        "email": usuario_actual.email,
        "rol": usuario_actual.rol
    }

# Eliminar Usuario (solo admin puede eliminar usuarios)
@router.delete("/usuarios/{usuario_id}", response_model=dict, tags=["Usuarios"])
def eliminar_usuario(usuario_id:int, session: SessionDep, _:Usuario = Depends[requerir_admin]):

    usuario = session.get(Usuario, usuario_id)

    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    session.delet(usuario)
    session.commit()
    return {"message": "Usuario eliminado correctamente"}