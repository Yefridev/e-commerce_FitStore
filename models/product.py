from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

class Producto(SQLModel, table=True):
    __tablename__ = "productos"

    id:           Optional[int] = Field(default=None, primary_key=True)
    categoria_id: Optional[int] = Field(default=None, foreign_key="categorias.id")
    nombre:       str           = Field(max_length=150)
    precio:       float         = Field(ge=0)
    descripcion:  Optional[str] = Field(default=None)
    stock:        int           = Field(default=0, ge=0)
    imagen:       Optional[str] = Field(default=None, max_length=300)
    created_at:   datetime      = Field(default_factory=datetime.now)