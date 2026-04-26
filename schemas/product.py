from pydantic import BaseModel
from typing import Optional


class ProductoCrear(BaseModel):
    nombre: str
    precio: float
    descripcion: str
    stock: int = 0
    imagen: Optional[str] = None


class ProductoActualizar(BaseModel):
    nombre: Optional[str] = None
    precio: Optional[float] = None
    descripcion: Optional[str] = None
    stock: Optional[int] = None
    imagen: Optional[str] = None


class ProductoRespuesta(BaseModel):
    id: int
    nombre: str
    precio: float
    descripcion: str
    stock: int
    imagen: str | None