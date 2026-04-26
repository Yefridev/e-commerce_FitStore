from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ProductoCreate(BaseModel):
    categoria_id: Optional[int] = None
    nombre:       str
    precio:       float
    descripcion:  Optional[str] = None
    stock:        int           = 0
    imagen:       Optional[str] = None

class ProductoUpdate(BaseModel):
    categoria_id: Optional[int]   = None
    nombre:       Optional[str]   = None
    precio:       Optional[float] = None
    descripcion:  Optional[str]   = None
    stock:        Optional[int]   = None
    imagen:       Optional[str]   = None

class ProductoResponse(BaseModel):
    id:           int
    categoria_id: Optional[int] = None
    nombre:       str
    precio:       float
    descripcion:  Optional[str] = None
    stock:        int
    imagen:       Optional[str] = None
    created_at:   datetime

    class Config:
        from_attributes = True