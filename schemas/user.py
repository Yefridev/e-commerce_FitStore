from pydantic import BaseModel, EmailStr
from typing import Optional


class UserBase(BaseModel):
    nombre: str
    email: EmailStr

# Modelo para crear usuario
class UserCreate(UserBase):
    password: str

# Modelo para login de usuario
class UserLogin(BaseModel):
    email: EmailStr
    password: str

# Modelo para respuesta de usuario
class UserResponse(BaseModel):
    id: int
    rol: str

    class Config:
        from_attributes = True

# Token (respuesta del login)
class Token(BaseModel):
    access_token: str
    token_type: str


# Datos dentro del token (opcional pero pro)
class TokenData(BaseModel):
    user_id: Optional[int] = None