from pydantic import BaseModel, Field

# Modelos para carrito de compras
class CartItemCreate(BaseModel):
    product_id: int
    quantity: int = Field(gt=0)

# Modelo para respuesta de carrito de compras
class CartItemResponse(BaseModel):
    product_id: int
    quantity: int