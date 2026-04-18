from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta
from config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")# Incriptar la contraseña

# hash de la contraseña
def hash_password(password: str):
    return pwd_context.hash(password)

# Verificar contraseña
def verify_password(plain, hashed):
    return pwd_context.verify(plain, hashed)
    
# Crear un token
def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.utcnow()+ timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update ({"exp": expire})

    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)