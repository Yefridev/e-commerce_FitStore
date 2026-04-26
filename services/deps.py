from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer
from sqlmodel import select, Session
from jose import jwt, JWTError
from database import SessionDep, get_session
from config import SECRET_KEY, ALGORITHM
from models.user import Usuario

security = HTTPBearer()


def obtener_usuario_actual(session: SessionDep, token=Depends(security)):
    try:
        payload = jwt.decode(token.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        usuario_id = payload.get("usuario_id")
        if usuario_id is None:
            raise HTTPException(status_code=401, detail="Token inválido")
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido o expirado")

    usuario = session.exec(select(Usuario).where(Usuario.id == usuario_id)).first()

    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    return usuario


def requerir_admin(usuario_actual: Usuario = Depends(obtener_usuario_actual)):
    if usuario_actual.rol != "admin":
        raise HTTPException(status_code=403, detail="No tienes permiso para realizar esta acción")
    return usuario_actual