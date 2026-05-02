from sqlmodel import SQLModel, Field
from typing import Optional
from sqlalchemy import Column, UniqueConstraint

class Categoria(SQLModel, table=True):
    __tablename__ = "categorias"
    __table_args__ = (UniqueConstraint("nombre"),)

    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str = Field(max_length=100, sa_column=Column("nombre", unique=True))
    descripcion: Optional[str] = Field(default=None)
