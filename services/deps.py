from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer
from sqlmodel import select
from jose import jwt, JWTError
from database import SessionDep
from config import SECRET_KEY, ALGORITHM

security = HTTPBearer()

def get_current_user(session: SessionDep, token=Depends(security)):
    try:
        payload = jwt.decode(token.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("user_id")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Token inválido")
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido o expirado")

    from models.user import Usuario
    user = session.exec(select(Usuario).where(Usuario.id == user_id)).first()

    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    return user