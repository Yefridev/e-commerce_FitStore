from pydantic import BaseModel
from typing import Optional

# Modelos para productos
class ProductCreate(BaseModel):
    nombre: str
    precio: float
    descripcion: str
    stock: int = 0
    imagen: Optional[str] = None

# Modelo para actualizar producto
class ProductUpdate(BaseModel):
    nombre: str
    precio: float

# Modelo para respuesta de producto
class ProductResponse(BaseModel):
    id: int
    nombre: str
    precio: float
    descripcion: str
    stock: int
    imagen: str | None