from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import select
from database import SessionDep
from models.target import Tarjeta
from schemas.target import TarjetaCreate
from services.deps import obtener_usuario_actual

router = APIRouter()

@router.post("/tarjeta/registro", response_model=dict, tags=["tarjeta"])
def registrar_tarjeta(datos: TarjetaCreate, session: SessionDep, usuario=Depends(obtener_usuario_actual)):
    try:
        nueva_tarjeta = Tarjeta(
            id_usuario=usuario.id,
            num_tarjeta=datos.numero_tarjeta,
            tipo_tarjeta=datos.tipo_tarjeta,
            fecha_exp=datos.fecha_expiracion,
            cod_cvv=datos.codigo_seguridad,
            saldo=datos.saldo,  # ✅ NUEVO: Guardar saldo inicial
            estado_tarjeta="activa"
        )
        
        session.add(nueva_tarjeta)
        session.commit()
        session.refresh(nueva_tarjeta)
        return {
            "message": "Tarjeta registrada con éxito", 
            "id": nueva_tarjeta.id,
            "saldo": nueva_tarjeta.saldo
        }
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=400, detail=f"Error al registrar tarjeta: {str(e)}")

@router.get("/tarjeta/mis-tarjetas", response_model=list, tags=["tarjeta"])
def obtener_tarjetas(session: SessionDep, usuario=Depends(obtener_usuario_actual)):
    tarjetas = session.exec(select(Tarjeta).where(Tarjeta.id_usuario == usuario.id)).all()
    return [
        {
            "id": t.id,
            "tipo_tarjeta": t.tipo_tarjeta,
            "num_tarjeta": t.num_tarjeta,
            "fecha_exp": t.fecha_exp,
            "saldo": t.saldo,  # ✅ NUEVO: Incluir saldo
            "estado_tarjeta": t.estado_tarjeta,
            "created_at": t.created_at
        }
        for t in tarjetas
    ]

@router.delete("/tarjeta/{tarjeta_id}", response_model=dict, tags=["tarjeta"])
def eliminar_tarjeta(tarjeta_id: int, session: SessionDep, usuario=Depends(obtener_usuario_actual)):
    tarjeta = session.exec(select(Tarjeta).where(Tarjeta.id == tarjeta_id)).first()
    
    if not tarjeta:
        raise HTTPException(status_code=404, detail="Tarjeta no encontrada")
    
    if tarjeta.id_usuario != usuario.id:
        raise HTTPException(status_code=403, detail="No tienes permiso para eliminar esta tarjeta")
    
    session.delete(tarjeta)
    session.commit()
    
    return {"message": "Tarjeta eliminada correctamente"}
