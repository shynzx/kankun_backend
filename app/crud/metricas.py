from app.schemas.metricas import cancelacionResponse, masReservadoResponse, IngresosResponse
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.reservas import Reserva
from sqlalchemy.future import select
from app.models.tours import Tour
from app.models.pagos import Pago
from sqlalchemy.sql import func
from datetime import datetime
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

async def get_ingresos_periodo(db: AsyncSession, fecha_inicio: datetime, fecha_fin: datetime):
    result = await db.execute(
        select(func.sum(Pago.costo_total_pago)).where(Pago.fecha_pago.between(fecha_inicio, fecha_fin))
    )
    sum_result = result.scalar()
    result_float = float(sum_result or 0.0)
    return IngresosResponse(ingresos_totales=result_float)