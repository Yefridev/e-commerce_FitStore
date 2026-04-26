from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta
from config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def crear_hash_password(password: str):
    return pwd_context.hash(password)


def verificar_password(texto_plano, hashed):
    return pwd_context.verify(texto_plano, hashed)
    

def crear_token_acceso(datos: dict):
    to_encode = datos.copy()

    expire = datetime.utcnow()+ timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update ({"exp": expire})

    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)