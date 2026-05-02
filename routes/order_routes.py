from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import select
from database import SessionDep
from models.order import Pedido, DetallePedido
from models.cart import Carrito, CarritoItem
from models.product import Producto
from models.address import Direccion
from models.user import Usuario
from schemas.order import PedidoCreate, PedidoResponse, PedidoEstadoUpdate, DetallePedidoResponse
from services.deps import obtener_usuario_actual, requerir_admin
from typing import List

router = APIRouter()


# Construir respuesta del pedido con items
def construir_respuesta_pedido(pedido: Pedido, session) -> PedidoResponse:
    detalles = session.exec(
        select(DetallePedido).where(DetallePedido.pedido_id == pedido.id)
    ).all()

    items = []
    for detalle in detalles:
        producto = session.get(Producto, detalle.producto_id)
        nombre = producto.nombre if producto else "Producto eliminado"
        items.append(DetallePedidoResponse(
            id=detalle.id,
            producto_id=detalle.producto_id,
            nombre=nombre,
            cantidad=detalle.cantidad,
            precio_unitario=detalle.precio_unitario,
            subtotal=round(detalle.precio_unitario * detalle.cantidad, 2)
        ))

    return PedidoResponse(
        id=pedido.id,
        usuario_id=pedido.usuario_id,
        direccion_id=pedido.direccion_id,
        estado=pedido.estado,
        total=pedido.total,
        created_at=pedido.created_at,
        items=items
    )


# Crear pedido desde el carrito
@router.post("/pedidos/", response_model=PedidoResponse, tags=["Pedidos"])
def create_pedido(datos: PedidoCreate, session: SessionDep, usuario_actual: Usuario = Depends(obtener_usuario_actual)):

    # Verificar que la dirección existe
    direccion = session.get(Direccion, datos.direccion_id)
    if not direccion:
        raise HTTPException(status_code=404, detail="Dirección no encontrada")
    if direccion.usuario_id != usuario_actual.id:
        raise HTTPException(status_code=403, detail="No tienes permiso para usar esta dirección")

    # Obtener el carrito del usuario
    carrito = session.exec(
        select(Carrito).where(Carrito.usuario_id == usuario_actual.id)
    ).first()

    if not carrito:
        raise HTTPException(status_code=400, detail="No tienes un carrito activo")

    # Obtener los items del carrito
    items_carrito = session.exec(
        select(CarritoItem).where(CarritoItem.carrito_id == carrito.id)
    ).all()

    if not items_carrito:
        raise HTTPException(status_code=400, detail="Tu carrito está vacío")

    # Verificar stock de los productos
    for item in items_carrito:
        producto = session.get(Producto, item.producto_id)
        if not producto:
            raise HTTPException(status_code=404, detail=f"Producto {item.producto_id} no encontrado")
        if producto.stock < item.cantidad:
            raise HTTPException(
                status_code=400,
                detail=f"Stock insuficiente para '{producto.nombre}'. Stock disponible: {producto.stock}"
            )

    # Calcular total
    total = 0.0
    for item in items_carrito:
        producto = session.get(Producto, item.producto_id)
        total += producto.precio * item.cantidad

    # Crear el pedido
    pedido = Pedido(
        usuario_id=usuario_actual.id,
        direccion_id=datos.direccion_id,
        estado="pendiente",
        total=round(total, 2)
    )
    session.add(pedido)
    session.commit()
    session.refresh(pedido)

    # Crear los detalles y descontar stock
    for item in items_carrito:
        producto = session.get(Producto, item.producto_id)

        detalle = DetallePedido(
            pedido_id=pedido.id,
            producto_id=item.producto_id,
            cantidad=item.cantidad,
            precio_unitario=producto.precio
        )
        session.add(detalle)

        # Descontar stock
        producto.stock -= item.cantidad
        session.add(producto)

    # Vaciar el carrito
    for item in items_carrito:
        session.delete(item)

    session.commit()

    return construir_respuesta_pedido(pedido, session)


# Ver mis pedidos
@router.get("/pedidos/", response_model=List[PedidoResponse], tags=["Pedidos"])
def get_pedidos(session: SessionDep, usuario_actual: Usuario = Depends(obtener_usuario_actual)):
    pedidos = session.exec(
        select(Pedido).where(Pedido.usuario_id == usuario_actual.id)
    ).all()
    return [construir_respuesta_pedido(p, session) for p in pedidos]


# Ver un pedido por ID
@router.get("/pedidos/{pedido_id}", response_model=PedidoResponse, tags=["Pedidos"])
def get_pedido(pedido_id: int, session: SessionDep, usuario_actual: Usuario = Depends(obtener_usuario_actual)):
    pedido = session.get(Pedido, pedido_id)

    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    if pedido.usuario_id != usuario_actual.id:
        raise HTTPException(status_code=403, detail="No tienes permiso para ver este pedido")

    return construir_respuesta_pedido(pedido, session)


# Ver todos los pedidos
@router.get("/admin/pedidos/", response_model=List[PedidoResponse], tags=["Pedidos"])
def get_todos_pedidos(session: SessionDep, _: Usuario = Depends(requerir_admin)):
    pedidos = session.exec(select(Pedido)).all()
    return [construir_respuesta_pedido(p, session) for p in pedidos]


# Actualizar estado del pedido
@router.put("/admin/pedidos/{pedido_id}/estado", response_model=PedidoResponse, tags=["Pedidos"])
def update_estado_pedido(pedido_id: int, datos: PedidoEstadoUpdate, session: SessionDep, _: Usuario = Depends(requerir_admin)):

    estados_validos = ["pendiente", "pagado", "enviado", "entregado", "cancelado"]
    if datos.estado not in estados_validos:
        raise HTTPException(
            status_code=400,
            detail=f"Estado inválido. Estados válidos: {', '.join(estados_validos)}"
        )

    pedido = session.get(Pedido, pedido_id)
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")

    pedido.estado = datos.estado
    session.add(pedido)
    session.commit()
    session.refresh(pedido)

    return construir_respuesta_pedido(pedido, session)