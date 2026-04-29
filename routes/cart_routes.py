from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import select
from datetime import datetime
from database import SessionDep
from models.cart import Carrito, CarritoItem
from models.product import Producto
from models.user import Usuario
from schemas.cart import CarritoItemAgregar, CarritoItemActualizar,CarritoItemRespuesta,CarritoRespuesta
from services.deps import obtener_usuario_actual

router = APIRouter()


# Obtener o crear carrito
def obtener_o_crear_carrito(usuario_id: int, session) -> Carrito:
    carrito = session.exec(
        select(Carrito).where(Carrito.usuario_id == usuario_id)
    ).first()

    if not carrito:
        carrito = Carrito(usuario_id=usuario_id)
        session.add(carrito)
        session.commit()
        session.refresh(carrito)

    return carrito

# Construir respuesta del carrito con items
def construir_respuesta_carrito(carrito: Carrito, session) -> CarritoRespuesta:
    items_db = session.exec(
        select(CarritoItem).where(CarritoItem.carrito_id == carrito.id)
    ).all()

    items = []
    total = 0.0

    for item in items_db:
        producto = session.get(Producto, item.producto_id)
        if producto:
            subtotal = producto.precio * item.cantidad
            total += subtotal
            items.append(CarritoItemRespuesta(
                id=item.id,
                producto_id=item.producto_id,
                cantidad=item.cantidad,
                nombre=producto.nombre,
                precio=producto.precio,
                subtotal=subtotal
            ))

    return CarritoRespuesta(
        id=carrito.id,
        usuario_id=carrito.usuario_id,
        items=items,
        total=round(total, 2)
    )

# Ver carrito
@router.get("/carrito/", response_model=CarritoRespuesta, tags=["Carrito"])
def ver_carrito(session: SessionDep, usuario_actual: Usuario = Depends(obtener_usuario_actual)):
    carrito = obtener_o_crear_carrito(usuario_actual.id, session)
    return construir_respuesta_carrito(carrito, session)

# Agregar producto al carrito
@router.post("/carrito/", response_model=CarritoRespuesta, tags=["Carrito"])
def agregar_al_carrito(item: CarritoItemAgregar, session: SessionDep, usuario_actual: Usuario = Depends(obtener_usuario_actual)):

    #Verificar que el producto existe y tiene stock
    producto = session.get(Producto,item.producto_id)
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    if producto.stock<item.cantidad:
        raise HTTPException(status_code=400, detail=f"Stock insuficiente. Stock disponible: {producto.stock}")
    
    carrito = obtener_o_crear_carrito(usuario_actual.id, session)

    # Si el producto ya está en el carrito
    item_existente = session.exce(
        select(CarritoItem).where(
            CarritoItem.carrito_id == carrito.id,
            CarritoItem.producto_id == item.producto_id
        )
    ).first()

    if item_existente:
        nueva_cantidad = item_existente.cantidad + item.cantidad

        if producto.stock < nueva_cantidad:
            raise HTTPException(status_code=400, detail= f"Stock insuficiente. Stock disponible: {producto.stock}")
        item_existente.cantidad = nueva_cantidad
        session.add(item_existente)

     # Actualizar fecha del carrito
    carrito.updated_at = datetime.now()
    session.add(carrito)
    session.commit()

    return construir_respuesta_carrito(carrito, session)

# Actualizar cantidad de un item
@router.put("/carrito/{item_id}", response_model=CarritoRespuesta, tags=["Carrito"])
def actualizar_item(item_id: int, datos: CarritoItemActualizar, session: SessionDep, usuario_actual: Usuario = Depends(obtener_usuario_actual)):

    carrito = obtener_o_crear_carrito(usuario_actual.id, session)

    item = session.exec(
        select(CarritoItem).where(
            CarritoItem.id == item_id,
            CarritoItem.carrito_id == carrito.id
        )
    ).first()

    if not item:
        raise HTTPException(status_code=404, detail="Item no encontrado en tu carrito")

    producto = session.get(Producto, item.producto_id)
    if producto.stock < datos.cantidad:
        raise HTTPException(status_code=400, detail=f"Stock insuficiente. Stock disponible: {producto.stock}")

    item.cantidad = datos.cantidad
    carrito.updated_at = datetime.now()
    session.add(item)
    session.add(carrito)
    session.commit()

    return construir_respuesta_carrito(carrito, session)


# Eliminar un item del carrito
@router.delete("/carrito/{item_id}", response_model=CarritoRespuesta, tags=["Carrito"])
def eliminar_item(item_id: int, session: SessionDep, usuario_actual: Usuario = Depends(obtener_usuario_actual)):

    carrito = obtener_o_crear_carrito(usuario_actual.id, session)

    item = session.exec(
        select(CarritoItem).where(
            CarritoItem.id == item_id,
            CarritoItem.carrito_id == carrito.id
        )
    ).first()

    if not item:
        raise HTTPException(status_code=404, detail="Item no encontrado en tu carrito")

    session.delete(item)
    carrito.updated_at = datetime.now()
    session.add(carrito)
    session.commit()

    return construir_respuesta_carrito(carrito, session)


# Vaciar el carrito completo
@router.delete("/carrito/", response_model=dict, tags=["Carrito"])
def vaciar_carrito(session: SessionDep, usuario_actual: Usuario = Depends(obtener_usuario_actual)):

    carrito = obtener_o_crear_carrito(usuario_actual.id, session)

    items = session.exec(
        select(CarritoItem).where(CarritoItem.carrito_id == carrito.id)
    ).all()

    for item in items:
        session.delete(item)

    carrito.updated_at = datetime.now()
    session.add(carrito)
    session.commit()

    return {"message": "Carrito vaciado correctamente"}