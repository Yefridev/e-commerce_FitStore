from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

class Tarjeta(SQLModel, table=True):
    __tablename__ = "tarjetas_pagos"

    id: Optional[int] = Field(default=None, primary_key=True)
    id_usuario: int = Field(foreign_key="usuarios.id")
    num_tarjeta: str = Field(max_length=16)
    tipo_tarjeta: str = Field(max_length=100)
    fecha_exp: str = Field(max_length=5)
    cod_cvv: str = Field(max_length=4)
    saldo: float = Field(default=0.0)  # ✅ NUEVO: Monto disponible en la tarjeta
    estado_tarjeta: str = Field(default="activa")
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)