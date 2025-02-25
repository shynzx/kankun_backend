from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import and_
from app.models.ticket import Ticket
from app.models.pagos import Pago
from app.models.tours import Tour
from app.models.usuarios import Usuario
from app.schemas.tickets import TicketCreate, TicketResponse
from fastapi import HTTPException
from datetime import datetime

async def get_ticket(db: AsyncSession, ticket_id: int):
    result = await db.execute(
        select(Ticket)
        .filter(Ticket.id_ticket == ticket_id)
    )
    return result.scalar_one_or_none()

async def get_tickets(db: AsyncSession, skip: int = 0, limit: int = 100):
    result = await db.execute(
        select(Ticket)
        .offset(skip)
        .limit(limit)
    )
    return result.scalars().all()

async def create_ticket(db: AsyncSession, ticket: TicketCreate):
    try:
        # Verificar que el pago existe y está completado
        pago_result = await db.execute(
            select(Pago)
            .filter(Pago.id_pago == ticket.id_pago)
        )
        pago = pago_result.scalar_one_or_none()
        
        if not pago:
            raise HTTPException(status_code=404, detail="Pago no encontrado")
        
        if pago.estado_pago != 'completed':
            raise HTTPException(status_code=400, detail="El pago no está completado")

        # Verificar que no existe un ticket para este pago
        existing_ticket = await db.execute(
            select(Ticket)
            .filter(Ticket.id_pago == ticket.id_pago)
        )
        if existing_ticket.scalar_one_or_none():
            raise HTTPException(status_code=400, detail="Ya existe un ticket para este pago")

        # Crear el ticket
        db_ticket = Ticket(
            fecha_ticket=datetime.utcnow(),
            total_ticket=pago.costo_total_pago,
            id_pago=pago.id_pago
        )
        
        db.add(db_ticket)
        await db.commit()
        await db.refresh(db_ticket)
        
        return db_ticket

    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

async def get_ticket_details(db: AsyncSession, ticket_id: int):
    try:
        # Obtener el ticket y toda la información relacionada
        result = await db.execute(
            select(
                Ticket, 
                Pago, 
                Tour, 
                Usuario
            )
            .join(Pago, Ticket.id_pago == Pago.id_pago)
            .join(Tour, Pago.id_tour == Tour.id_tour)
            .join(Usuario, Pago.id_usuario == Usuario.id_usuario)
            .filter(Ticket.id_ticket == ticket_id)
        )
        
        record = result.first()
        if not record:
            raise HTTPException(status_code=404, detail="Ticket no encontrado")
            
        ticket, pago, tour, usuario = record
        
        return {
            "ticket_info": {
                "id_ticket": ticket.id_ticket,
                "fecha_ticket": ticket.fecha_ticket,
                "total_ticket": ticket.total_ticket
            },
            "pago_info": {
                "id_pago": pago.id_pago,
                "metodo_pago": pago.metodo_pago,
                "estado_pago": pago.estado_pago,
                "fecha_pago": pago.fecha_pago
            },
            "tour_info": {
                "nombre_tour": tour.nombre_tour,
                "tipo_tour": tour.tipo_tour,
                "dias_tour": tour.dias_tour,
                "direccion_inicio": tour.direccion_inicio_tour,
                "direccion_destino": tour.direccion_destino_tour
            },
            "cliente_info": {
                "usuario": usuario.nombre_usuario,
                "correo": usuario.correo_usuario,
                "telefono": usuario.telefono_usuario
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))