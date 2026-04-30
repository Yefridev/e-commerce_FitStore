from pydantic import BaseModel, Field
from typing import Optional


class CarritoItemAgregar(BaseModel):
    producto_id: int
    cantidad: int = Field(ge=1)


class CarritoItemActualizar(BaseModel):
    cantidad: int = Field(ge=1)

class CarritoItemRespuesta(BaseModel):
    id: int
    producto_id: int
    cantidad: int
    nombre: str
    precio: float
    subtotal: float

    class Config:
        from_attributes = True

class CarritoRespuesta(BaseModel):
    id: int
    usuario_id: int
    items: list[CarritoItemRespuesta] = []
    total: float = 0.0