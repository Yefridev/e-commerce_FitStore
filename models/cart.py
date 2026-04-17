from typing import list, Dict
from schemas.cart import CartItemCreate

# Carrito de compras en memoria
carts: Dict[int, List[CartItemCreate]] = {}
