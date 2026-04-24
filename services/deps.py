from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer
from sqlmodel import select,Session
from jose import jwt, JWTError
from database import SessionDep, get_session
from config import SECRET_KEY, ALGORITHM
from models.user import Usuario

security = HTTPBearer()

# Función para obtener el usuario actual a partir del token JWT
def get_current_user(session: SessionDep, token=Depends(security)):
    try:
        payload = jwt.decode(token.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("user_id")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Token inválido")
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido o expirado")

    user = session.exec(select(Usuario).where(Usuario.id == user_id)).first()

    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    return user

# Función para verificar si el usuario tiene rol de admin
def require_admin(current_user: Usuario =Depends(get_current_user)):
    if current_user.rol != "admin":
        raise HTTPException(status_code=403, detail="No tienes permiso para realizar esta acción")
    return current_user