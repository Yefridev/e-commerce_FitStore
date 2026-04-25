from fastapi import APIRouter, HTTPException
from models.cart import carts
from schemas.cart import CartItemCreate, CartItemResponse
from services.utils import product_exists

router = APIRouter()

@router.get("/cart/{user_id}")
def get_cart(user_id: int):
    return carts.get(user_id, [])

@router.post("/cart/{user_id}")
def add_to_cart(user_id: int, item: CartItemCreate):
    
    if not product_exists(item.product_id):
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    
    if user_id not in carts:
        carts[user_id] = []
    
    for i, cart_item in enumerate(carts[user_id]):
        if cart_item.product_id == item.product_id:
            carts[user_id][i] = CartItemCreate(
                product_id=cart_item.product_id,
                quantity=cart_item.quantity + item.quantity
            )
            break
    else:
        carts[user_id].append(item)
    
    return {"message": "Producto agregado al carrito"}

@router.delete("/cart/{user_id}")
def remove_from_cart(user_id: int, product_id: int):
    if user_id not in carts:
        raise HTTPException(status_code=404, detail="Carrito no encontrado")
    
    original_len = len(carts[user_id])
    carts[user_id] = [i for i in carts[user_id] if i.product_id != product_id]

    if len(carts[user_id]) == original_len:
        raise HTTPException(status_code=404, detail="Producto no encontrado en el carrito")
    
    return {"message": "Producto eliminado del carrito"}