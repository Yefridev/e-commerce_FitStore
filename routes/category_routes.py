from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import select
from database import SessionDep
from models.category import Categoria
from models.user import Usuario
from schemas.category import CrearCategoria, RespuestaCategoria, ActualizarCategoria
from services.deps import requerir_admin


router = APIRouter()

# Obtener todas las categorías
@router.get("/categorias/", response_model=list[RespuestaCategoria], tags=["Categorías"])
def obtener_categorias(session: SessionDep):
    categorias = session.exec(select(Categoria)).all()
    return categorias

# Obtener categoría por ID
@router.get("/categorias/{categoria_id}", response_model=RespuestaCategoria, tags=["Categorías"])
def obtener_categoria(categoria_id: int, session: SessionDep):
    categoria = session.get(Categoria, categoria_id)
    if not categoria:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    return categoria

# Crear nueva categoría (solo admin puede crear categorías)
@router.post("/categorias/", response_model=RespuestaCategoria, tags=["Categorías"])
def crear_categoria(categoria: CrearCategoria, session: SessionDep, _: Usuario = Depends(requerir_admin)):
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

# Actualizar categoría (solo admin puede actualizar categorías)
@router.put("/categorias/{categoria_id}", response_model=RespuestaCategoria, tags=["Categorías"])
def actualizar_categoria(categoria_id: int, datos: ActualizarCategoria, session: SessionDep, _: Usuario = Depends(requerir_admin)):

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

# Eliminar categoría (solo admin puede eliminar categorías)
@router.delete("/categorias/{categoria_id}", response_model=dict, tags=["Categorías"])
def eliminar_categoria(categoria_id: int, session: SessionDep, _: Usuario = Depends(requerir_admin)):

    categoria = session.get(Categoria, categoria_id)

    if not categoria:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")

    session.delete(categoria)
    session.commit()
    return {"message": "Categoría eliminada correctamente"}