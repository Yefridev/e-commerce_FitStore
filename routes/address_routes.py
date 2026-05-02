from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import select
from database import SessionDep
from models.address import Direccion
from models.user import Usuario
from schemas.address import DireccionCreate, DireccionUpdate, DireccionResponse
from services.deps import obtener_usuario_actual
from typing import List

router = APIRouter()

#Ver mis direcciones
@router.get("/direcciones/", response_model=List[DireccionResponse], tags=["Direcciones"])
def get_direcciones(session: SessionDep, usuario_actual: Usuario = Depends(obtener_usuario_actual)):
    direcciones =  session.exec(
        select(Direccion).where(Direccion.usuario_id == usuario_actual.id)
    ).all()
    return direcciones

# Ver uan dirección por ID
@router.get("/direcciones/{direcciones_id}", response_model=DireccionResponse, tags=["Direcciones"])
def get_direccion(direccion_id: int, session: SessionDep, usuario_actual: Usuario = Depends(obtener_usuario_actual)):
    direccion = session.get(Direccion, direccion_id)

    if not direccion:
        raise HTTPException(status_code=404, detail="Dirección no encontrada")
    if direccion.usuario_id != usuario_actual.id:
        raise HTTPException(status_code=403, detail="No tienes permiso para ver esta dirección.")
    
    return direccion

# Crear dirección
@router.post("/direcciones/", response_model=DireccionResponse, tags=["Direcciones"])
def create_direccion(datos: DireccionCreate, session: SessionDep, usuario_actual: Usuario = Depends(obtener_usuario_actual)):

    if datos.es_principal:
        direcciones_actules = session.exec(
            select(Direccion).where(Direccion.usuario_id == usuario_actual.id)
        ).all()

        for d in direcciones_actules:
            d.es_principal = False
            session.add(d)

    nueva = Direccion(
        usuario_id=usuario_actual.id,
        calle=datos.calle,
        ciudad=datos.ciudad,
        departamento=datos.departamento,
        codigo_postal=datos.codigo_postal,
        es_principal=datos.es_principal
    )

    session.add(nueva)
    session.commit()
    session.refresh(nueva)
    return nueva

# Actualizar dirección
@router.put("/direcciones/{direccion_id}", response_model=DireccionResponse, tags=["Direcciones"])
def update_direccion(direccion_id: int, datos:DireccionUpdate, session: SessionDep, usuario_actual: Usuario = Depends(obtener_usuario_actual)):

    direccion = session.get(Direccion, direccion_id)

    if not direccion:
        raise HTTPException(status_code=404, detail="Direccion no encontrada")
    
    if direccion.usuario_id != usuario_actual.id:
        raise HTTPException(status_code=403, detail="No tienes permiso para editar esta direccion")
    
    if datos.es_principal:
        otras = session.exec(
            select(Direccion).where(
                Direccion.usuario_id == usuario_actual.id,
                Direccion.id != direccion_id
            )
        ).all()

        for d in otras:
            d.es_principal = False
            session.add(d)

    if datos.calle is not None:
        direccion.calle = datos.calle
    if datos.ciudad is not None:
        direccion.ciudad = datos.ciudad
    if datos.departamento is not None:
        direccion.departamento = datos.departamento
    if datos.codigo_postal is not None:
        direccion.codigo_postal = datos.codigo_postal
    if datos.es_principal is not None:
        direccion.es_principal = datos.es_principal

    session.add(direccion)
    session.commit()
    session.refresh(direccion)
    return direccion
   

# Eliminar dirección
@router.delete("/direcciones/{direccion_id}", response_model=dict, tags=["Direcciones"])
def delete_direccion(direccion_id: int, session: SessionDep, usuario_actual: Usuario = Depends(obtener_usuario_actual)):

    direccion = session.get(Direccion, direccion_id)

    if not direccion:
        raise HTTPException(status_code=404, detail="Dirección no encontrada")
    
    if direccion.usuario_id != usuario_actual.id:
        raise HTTPException(status_code=403, detail="No tienes permiso para eliminar esta dirección")

    session.delete(direccion)
    session.commit()
    return {"message": "Dirección eliminada correctamente"}