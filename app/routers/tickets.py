from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.crud import tickets as tickets_crud
from app.schemas.tickets import TicketCreate, TicketResponse, TicketDetail
from app.models.db_connect import get_session

router = APIRouter(prefix='/tickets', tags=['Tickets'])

@router.get("/", response_model=List[TicketResponse],
    summary="Obtener lista de tickets",
    response_description="Lista de tickets con su información básica"
)
async def get_tickets(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_session)
):
    """
    Recupera una lista de todos los tickets en el sistema:

    - **skip**: Número de registros a saltar (para paginación)
    - **limit**: Número máximo de registros a devolver (para paginación)

    Devuelve una lista de tickets con:
    - ID del ticket
    - Fecha de emisión
    - Monto total
    - ID del pago asociado
    """
    return await tickets_crud.get_tickets(db, skip=skip, limit=limit)

@router.get("/{ticket_id}", response_model=TicketDetail,
    summary="Obtener detalles de un ticket",
    response_description="Información detallada del ticket incluyendo datos del tour, pago y cliente"
)
async def get_ticket_detail(
    ticket_id: int,
    db: AsyncSession = Depends(get_session)
):
    """
    Recupera información detallada de un ticket específico:

    - **ticket_id**: ID del ticket a consultar

    Devuelve información completa incluyendo:
    1. Información del Ticket:
        - ID del ticket
        - Fecha de emisión
        - Monto total
    2. Información del Pago:
        - ID del pago
        - Método de pago
        - Estado del pago
        - Fecha del pago
    3. Información del Tour:
        - Nombre del tour
        - Tipo de tour
        - Duración en días
        - Punto de inicio
        - Destino
    4. Información del Cliente:
        - Nombre de usuario
        - Correo electrónico
        - Teléfono
    """
    return await tickets_crud.get_ticket_details(db, ticket_id)

@router.post("/", response_model=TicketResponse,
    summary="Crear nuevo ticket",
    response_description="Ticket creado exitosamente"
)
async def create_ticket(
    ticket: TicketCreate,
    db: AsyncSession = Depends(get_session)
):
    """
    Crea un nuevo ticket para un pago completado:

    - **id_pago**: ID del pago para el cual se generará el ticket

    El proceso realiza las siguientes acciones:
    1. Verifica que el pago exista y esté completado
    2. Verifica que no exista un ticket previo para este pago
    3. Genera un nuevo ticket con:
        - Fecha actual de emisión
        - Monto total del pago
        - Referencia al pago

    Devuelve:
    - Información del ticket creado incluyendo su ID
    - Fecha de emisión
    - Monto total

    Si el pago no existe o no está completado, se devolverá un error.
    Si ya existe un ticket para este pago, se devolverá un error.
    """
    return await tickets_crud.create_ticket(db, ticket)