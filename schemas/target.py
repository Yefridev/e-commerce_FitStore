from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional

class TarjetaBase(SQLModel):
    tipo_tarjeta: str = Field(max_length=100)
    numero_tarjeta: str = Field(max_length=16)
    fecha_expiracion: str = Field(max_length=5)
    codigo_seguridad: str = Field(max_length=4)
    saldo: float = Field(default=0.0)  # ✅ NUEVO: Saldo inicial

class TarjetaCreate(TarjetaBase):
    pass

class TarjetaResponse(SQLModel):
    id: int
    tipo_tarjeta: str
    num_tarjeta: str
    fecha_exp: str
    saldo: float  # ✅ NUEVO: Mostrar saldo en respuestas
    estado_tarjeta: str
    created_at: datetime
