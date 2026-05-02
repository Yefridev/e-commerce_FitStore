from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class DetallePedidoResponse(BaseModel):
    id: int
    producto_id: int
    nombre: str
    cantidad: int
    precio_unitario: float
    subtotal: float

    class Config:
        from_attributes = True

class PedidoCreate(BaseModel):
    direccion_id: int

class PedidoResponse(BaseModel):
    id: int
    usuario_id: int
    direccion_id: int
    estado: str
    total: float
    created_at: datetime
    items: List[DetallePedidoResponse] = []

    class Config:
        from_attributes = True

class PedidoEstadoUpdate(BaseModel):
    estado: str