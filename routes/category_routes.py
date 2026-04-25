from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import select
from database import SessionDep
from models.category import Categoria
from models.user import Usuario
from schemas.category import CategoriaCreate, CategoriaResponse, CategoriaUpdate
from services.deps import require_admin




router = APIRouter()

# Ver todas las categorias
@router.get("/categorias/", response_model=list[CategoriaResponse], tags=["Categorías"])
def get_categorias(session:SessionDep):
    categorias = session.exec(select(Categoria)).all()
    return categorias

# Ver categoria por ID
@router.get("/categorias/{categoria_id}", response_model=CategoriaResponse, tags = ["Categorías"])
def get_categoria(categoria_id: int, session: SessionDep):
    categoria = session.get(Categoria, categoria_id)
    if not categoria:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    return categoria

# Crear categoria
@router.post("/categorias/", response_model=CategoriaResponse, tags=["Categorías"])
def create_categoria(categoria: CategoriaCreate, session: SessionDep, _:Usuario = Depends(require_admin)):
    existe = session.exec(select(Categoria).where(Categoria.nombre == categoria.nombre)).first()

    if existe:
        raise HTTPException(status_code=400, detail="La categoría ya existe")
    
    nueva = Categoria(
        nombre=categoria.nombre,
        descripcion=categoria.descripcion
    )

    session.add(nueva)
    session.commit()
    session.refresh(nueva)
    return nueva

# Editar categoria (admin)
@router.put("/categorias/{categoria_id}", response_model=CategoriaResponse, tags=["Categorías"])
def update_categoria(categoria_id: int, datos: CategoriaUpdate, session: SessionDep, _:Usuario = Depends(require_admin)):

    categoria = session.get(Categoria, categoria_id)
    if not categoria:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    
    if datos.nombre is not None:
        categoria.nombre = datos.nombre
    if datos.descripcion is not None:
        categoria.descripcion = datos.descripcion

    session.add(categoria)
    session.commit()
    session.refresh(categoria)
    return categoria

# Eliminar categoría (admin)
@router.delete("/categorias/{categoria_id}", response_model=dict,tags=["Categorías"] )
def delete_categoria(categoria_id: int, session: SessionDep, _: Usuario = Depends(require_admin)):

    categoria = session.get(Categoria, categoria_id)

    if not categoria:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")

    session.delete(categoria)
    session.commit()
    return {"message": "Categoría eliminada correctamente"}