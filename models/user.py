from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

class Usuario(SQLModel, table=True):
    __tablename__ = "usuarios"

    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str = Field (max_length=100)
    email: str = Field(max_length=150)
    password: str = Field(max_length=255)
    rol: str = Field(default="cliente", max_length=20)
    created_at: datetime = Field(default_factory=datetime.now)