from pydantic import BaseModel
from typing import Optional

class DireccionCreate(BaseModel):
    calle: str
    ciudad: str
    departamento: str
    codigo_postal: Optional[str] = None
    es_principal: bool = False

class DireccionUpdate(BaseModel):
    calle:  Optional[str] = None
    ciudad:  Optional[str] = None
    departamento:  Optional[str] = None
    codigo_postal: Optional[str] = None
    es_principal:  Optional[bool] = None

class DireccionResponse(BaseModel):
    id: int
    usuario_id: int
    calle: str
    ciudad: str
    departamento: str
    codigo_postal: Optional[str] = None
    es_principal: bool

    class Config:
        from_attributes = True
