from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer
from jose import jwt, JWTError
from database import get_connection
from config import SECRET_KEY, ALGORITHM

security = HTTPBearer()

def get_current_user(token: str = Depends(security)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("user_id")

        if user_id is None:
            raise HTTPException(status_code=401, detail="Token inválido")

    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido o expirado")

    conexion = get_connection()

    if not conexion:
        raise HTTPException(status_code=500, detail="Error de conexión a la base de datos")

    cursor = None
    try:
        cursor = conexion.cursor(dictionary=True)
        cursor.execute("SELECT * FROM usuarios WHERE id = %s", (user_id,))
        user = cursor.fetchone()
    finally:
        if cursor:
            cursor.close()
        conexion.close()

    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado.")

    return user