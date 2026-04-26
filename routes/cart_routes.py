from fastapi import APIRouter, HTTPException
from models.cart import carritos
from schemas.cart import ItemCarritoCrear, ItemCarritoRespuesta
from services.utils import existe_producto

router = APIRouter()


@router.get("/carrito/{usuario_id}")
def obtener_carrito(usuario_id: int):
    return carritos.get(usuario_id, [])


@router.post("/carrito/{usuario_id}")
def agregar_al_carrito(usuario_id: int, item: ItemCarritoCrear):
    
    if not existe_producto(item.producto_id):
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    
    if usuario_id not in carritos:
        carritos[usuario_id] = []
    
    for i, item_carrito in enumerate(carritos[usuario_id]):
        if item_carrito.producto_id == item.producto_id:
            carritos[usuario_id][i] = ItemCarritoCrear(
                producto_id=item_carrito.producto_id,
                cantidad=item_carrito.cantidad + item.cantidad
            )
            break
    else:
        carritos[usuario_id].append(item)
    
    return {"message": "Producto agregado al carrito"}


@router.delete("/carrito/{usuario_id}")
def eliminar_del_carrito(usuario_id: int, producto_id: int):
    if usuario_id not in carritos:
        raise HTTPException(status_code=404, detail="Carrito no encontrado")
    
    longitud_original = len(carritos[usuario_id])
    carritos[usuario_id] = [i for i in carritos[usuario_id] if i.producto_id != producto_id]

    if len(carritos[usuario_id]) == longitud_original:
        raise HTTPException(status_code=404, detail="Producto no encontrado en el carrito")
    
    return {"message": "Producto eliminado del carrito"}