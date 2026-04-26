from pydantic import BaseModel
from typing import Optional


class CrearCategoria(BaseModel):
    nombre: str
    descripcion: Optional[str] = None


class ActualizarCategoria(BaseModel):
    nombre: Optional[str]
    descripcion: Optional[str] = None


class RespuestaCategoria(BaseModel):
    id: int
    nombre: str
    descripcion: Optional[str] = None

    class Config:
        from_attributes = True