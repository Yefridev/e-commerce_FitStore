from pydantic import BaseModel, EmailStr
from typing import Optional


class UsuarioBase(BaseModel):
    nombre: str
    email: EmailStr


class UsuarioCrear(UsuarioBase):
    password: str


class UsuarioLogin(BaseModel):
    email: EmailStr
    password: str


class UsuarioRespuesta(BaseModel):
    id: int
    rol: str

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str


class DatosToken(BaseModel):
    usuario_id: Optional[int] = None