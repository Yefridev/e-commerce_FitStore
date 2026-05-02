from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

class Pedido(SQLModel, table=True):
    __tablename__ = "pedidos"

    id: Optional[int] = Field(default=None, primary_key=True)
    usuario_id: int = Field(foreign_key="usuarios.id")
    direccion_id: int = Field(foreign_key="direcciones.id")
    estado:str = Field(default="pendiente", max_length=30)
    total: float = Field(default=0.0, ge=0)
    created_at: datetime = Field(default_factory=datetime.now)


class DetallePedido(SQLModel, table=True):
    __tablename__ = "detalle_pedidos"

    id: Optional[int] = Field(default=None, primary_key=True)
    pedido_id: int = Field(foreign_key="pedidos.id")
    producto_id: int = Field(foreign_key="productos.id")
    cantidad: int = Field(ge=1)
    precio_unitario: float = Field(ge=0)