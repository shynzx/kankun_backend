from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.crud import reservas as reservas_crud
from app.schemas.reservas import ReservaCreate, ReservaResponse, ReservaUpdate
from app.models.db_connect import get_session

router = APIRouter(prefix='/reservas', tags=['Reservas'])

@router.get("/", response_model=List[ReservaResponse])
async def get_reservas(
    skip: int = 0, 
    limit: int = 100, 
    db: AsyncSession = Depends(get_session)
):
    return await reservas_crud.get_reservas(db, skip=skip, limit=limit)

@router.get("/{reserva_id}", response_model=ReservaResponse)
async def get_reserva(
    reserva_id: int, 
    db: AsyncSession = Depends(get_session)
):
    reserva = await reservas_crud.get_reserva(db, reserva_id)
    if reserva is None:
        raise HTTPException(status_code=404, detail="Reserva no encontrada")
    return reserva

@router.post("/", response_model=ReservaResponse)
async def create_reserva(
    reserva: ReservaCreate, 
    db: AsyncSession = Depends(get_session),
):
    return await reservas_crud.create_reserva(db, reserva)

@router.put("/{reserva_id}", response_model=ReservaResponse)
async def update_reserva(
    reserva_id: int, 
    reserva: ReservaUpdate, 
    db: AsyncSession = Depends(get_session),
):
    updated_reserva = await reservas_crud.update_reserva(db, reserva_id, reserva)
    if updated_reserva is None:
        raise HTTPException(status_code=404, detail="Reserva no encontrada")
    return updated_reserva

@router.delete("/{reserva_id}")
async def delete_reserva(
    reserva_id: int, 
    db: AsyncSession = Depends(get_session),
):
    success = await reservas_crud.delete_reserva(db, reserva_id)
    if not success:
        raise HTTPException(status_code=404, detail="Reserva no encontrada")
    return {"message": "Reserva eliminada correctamente"}

@router.post("/{reserva_id}/confirm")
async def confirm_reserva(
    reserva_id: int, 
    db: AsyncSession = Depends(get_session),
):
    success = await reservas_crud.confirm_reservation(db, reserva_id)
    if not success:
        raise HTTPException(status_code=400, detail="No se pudo confirmar la reserva")
    return {"message": "Reserva confirmada correctamente"}

@router.post("/{reserva_id}/cancel")
async def cancel_reserva(
    reserva_id: int, 
    db: AsyncSession = Depends(get_session),
):
    success = await reservas_crud.cancel_reservation(db, reserva_id)
    if not success:
        raise HTTPException(status_code=400, detail="No se pudo cancelar la reserva")
    return {"message": "Reserva cancelada correctamente"}
