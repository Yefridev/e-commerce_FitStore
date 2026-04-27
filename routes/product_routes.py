from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import select
from database import SessionDep
from models.product import Producto
from models.category import Categoria
from models.user import Usuario
from schemas.product import ProductoCreate, ProductoUpdate, ProductoResponse
from services.deps import requerir_admin
from typing import List

router = APIRouter()

# Ver todos los productos — cualquiera puede verlos
@router.get("/productos/", response_model=List[ProductoResponse], tags=["Productos"])
def get_productos(session: SessionDep):
    productos = session.exec(select(Producto)).all()
    return productos

# Ver un producto por ID
@router.get("/productos/{producto_id}", response_model=ProductoResponse, tags=["Productos"])
def get_producto(producto_id: int, session: SessionDep):
    producto = session.get(Producto, producto_id)
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return producto

# Ver productos por categoría — valida que la categoría exista
@router.get("/productos/categoria/{categoria_id}", response_model=List[ProductoResponse], tags=["Productos"])
def get_productos_por_categoria(categoria_id: int, session: SessionDep):
    categoria = session.get(Categoria, categoria_id)
    if not categoria:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    productos = session.exec(
        select(Producto).where(Producto.categoria_id == categoria_id)
    ).all()
    return productos

# Crear producto — solo admin, valida que la categoría exista
@router.post("/productos/", response_model=ProductoResponse, status_code=201, tags=["Productos"])
def create_producto(producto: ProductoCreate, session: SessionDep, _: Usuario = Depends(requerir_admin)):
    if producto.categoria_id:
        categoria = session.get(Categoria, producto.categoria_id)
        if not categoria:
            raise HTTPException(status_code=404, detail="Categoría no encontrada")

    nuevo = Producto(
        categoria_id=producto.categoria_id,
        nombre=producto.nombre,
        precio=producto.precio,
        descripcion=producto.descripcion,
        stock=producto.stock,
        imagen=producto.imagen
    )
    session.add(nuevo)
    session.commit()
    session.refresh(nuevo)
    return nuevo

# Actualizar producto — solo admin
@router.put("/productos/{producto_id}", response_model=ProductoResponse, tags=["Productos"])
def update_producto(producto_id: int, datos: ProductoUpdate, session: SessionDep, _: Usuario = Depends(requerir_admin)):
    producto = session.get(Producto, producto_id)
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    for campo, valor in datos.model_dump(exclude_unset=True).items():
        setattr(producto, campo, valor)

    session.add(producto)
    session.commit()
    session.refresh(producto)
    return producto

# Eliminar producto — solo admin
@router.delete("/productos/{producto_id}", tags=["Productos"])
def delete_producto(producto_id: int, session: SessionDep, _: Usuario = Depends(requerir_admin)):
    producto = session.get(Producto, producto_id)
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    session.delete(producto)
    session.commit()
    return {"message": "Producto eliminado correctamente"}