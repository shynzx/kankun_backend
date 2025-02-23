from fastapi import APIRouter, HTTPException, Depends, Request
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.db_connect import get_session
from app.crud.metricas import get_porcentaje_cancelaciones, get_tours_mas_reservados
from typing import List
from app.schemas.metricas import *

router = APIRouter(prefix='/metricas', tags=["Metricas"])

@router.get("/cancelaciones", response_model=List[cancelacionResponse])
async def get_cancelaciones(
        db: AsyncSession = Depends(get_session)
    ):
        cancelaciones = await get_porcentaje_cancelaciones(db)
        
        if not cancelaciones:
            raise HTTPException(status_code=404, detail="Aún no hay reservas!")
        
        return cancelaciones
    
@router.get("/masReservados", response_model=List[masReservadoResponse])
async def get_reservados(
    db: AsyncSession = Depends(get_session),
    limit: int = 10
):
    if limit <= 0:
        raise HTTPException(status_code=400, detail="El limite debe ser mayor que 0!")

    reservados = await get_tours_mas_reservados(db, limit)
    
    if not reservados:
        raise HTTPException(status_code=404, detail="Aún no hay reservas!")
    
    return reservados