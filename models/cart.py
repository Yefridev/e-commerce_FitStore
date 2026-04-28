from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

# Modelos para el carrito de compras
class Carrito(SQLModel, table=True):
    __tablename__= "carritos"

    id: Optional[int] = Field(default=None, primary_key=True)
    usuario_id: int = Field(foreign_key=["usuarios.id"])
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

# Modelo para los items del carrito
class CarritoItem(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True) 
    carrito_id: int = Field(foreign_key=["carritos.id"])
    producto_id: int = Field(foreign_key=["productos.id"])
    cantidad: int = Field(default=1, ge=1) # Cantidad mínima de 1