from sqlmodel import SQLModel, Field
from typing import Optional

class Direccion(SQLModel, table=True):
    __tablename__= "direcciones"

    id: Optional[int] = Field(default=None, primary_key=True)
    usuario_id: int = Field(foreign_key="usuarios.id")
    calle: str = Field (max_length=200)
    ciudad: str = Field(max_length=100)
    departamento: str = Field(max_length=100)
    codigo_postal: Optional[str] = Field(default=None, max_length=20)
    es_principal: bool = Field(default=False)