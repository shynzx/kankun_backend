from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import func
from sqlalchemy.future import select
from app.schemas.metricas import cancelacionResponse
from app.models.reservas import Reserva
from app.models.tours import Tour
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import func
from app.schemas.metricas import masReservadoResponse
from typing import List

async def get_porcentaje_cancelaciones(db: AsyncSession):
    
    cancelado_result = await db.execute(
        select(func.count()).where(Reserva.estatus == "cancelado")
    )
    cancelado_count = cancelado_result.scalar() or 0  

    
    total_result = await db.execute(select(func.count()).select_from(Reserva))
    total_count = total_result.scalar() or 1  

    
    percentage = (cancelado_count / total_count) * 100

    return [cancelacionResponse(reservasCanceladas= cancelado_count, reservasCanceladasPorcentaje=percentage, reservasTotal= total_count)]

async def get_tours_mas_reservados(db: AsyncSession, limit: int = 10) -> List[masReservadoResponse]:
    result = await db.execute(
        select(Reserva.id_tour, Tour.nombre_tour, func.count(Reserva.id_reserva).label("reservas_totales"))
        .join(Tour, Reserva.id_tour == Tour.id_tour)  # Join para obtener el nombre del tour
        .group_by(Reserva.id_tour, Tour.nombre_tour)
        .order_by(func.count(Reserva.id_reserva).desc())  
        .limit(limit)  # Limit para el top 10
    )

    # Convert query result into Pydantic models
    return [masReservadoResponse(tour_id=row[0], tour_name=row[1], total_reservations=row[2]) for row in result.all()]