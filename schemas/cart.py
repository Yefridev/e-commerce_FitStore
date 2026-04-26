from pydantic import BaseModel, Field


class ItemCarritoCrear(BaseModel):
    producto_id: int
    cantidad: int = Field(gt=0)


class ItemCarritoRespuesta(BaseModel):
    producto_id: int
    cantidad: int