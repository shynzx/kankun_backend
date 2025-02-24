from fastapi import APIRouter, HTTPException, Depends, Request
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.db_connect import get_session
from app.crud.metricas import *
from typing import List
from app.schemas.metricas import *

router = APIRouter(prefix='/metricas', tags=["Metricas"])

@router.get("/cancelaciones", response_model=List[cancelacionResponse])
async def get_cancelaciones(
        db: AsyncSession = Depends(get_session)
    ):
        """
        Busca todas las instancias de cancelaciones dentro de las reservas, las cuenta y posteriormente regresa el número total de reservas, la cantidad de cancelaciones, y el porcentaje de cancelaciones:
    
        """
        try:
            cancelaciones = await get_porcentaje_cancelaciones(db)
            
            if not cancelaciones:
                raise HTTPException(status_code=404, detail="Aún no hay reservas!")
            
            return cancelaciones
    
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error al realizar la operación: {str(e)}")
    
@router.get("/masReservados", response_model=List[masReservadoResponse])
async def get_reservados(
    db: AsyncSession = Depends(get_session),
    limit: int = 10
):
    """
    Busca todas las reservas, y cuenta la cantidad de veces que se ha reservado un tour, posteriormente retorna los tours con su id, nombre y veces que se han reservado en una lista que va del mayor al menor:

    - **limit**: cantidad de tours que son retornados, por defecto, 10.
    
    """
    if limit <= 0:
        raise HTTPException(status_code=400, detail="El limite debe ser mayor que 0!")
    
    try:

        reservados = await get_tours_mas_reservados(db, limit)
    
        if not reservados:
            raise HTTPException(status_code=404, detail="Aún no hay reservas!")
    
        return reservados
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al realizar la operación: {str(e)}")

@router.get("/ingresos_periodo", response_model=IngresosResponse)
async def get_ingresos(
    db: AsyncSession = Depends(get_session),
    fecha_inicio: datetime = datetime.today().replace(day=1),  # Primer día del mes
    fecha_final: datetime = datetime.today()
):
    """
    Busca los pagos dentro del periodo de tiempo estipulado y posteriormente retorna la suma de todos los ingresos:

    - **fecha_inicio**: fecha desde donde se inicia la busqueda, por defecto, el primer día del mes.
    - **fecha_final**: fecha donde se detiene la busqueda, por defecto, el día actual.
    
    """
    
    if fecha_inicio > fecha_final:
        raise HTTPException(status_code=400, detail="La fecha de inicio no puede ser mayor que la fecha final!")

    try:
        ingresos = await get_ingresos_periodo(db, fecha_inicio, fecha_final)
        return ingresos
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al realizar la operación: {str(e)}")