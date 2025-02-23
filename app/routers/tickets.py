from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.crud import tickets as tickets_crud
from app.schemas.tickets import TicketCreate, TicketResponse, TicketDetail
from app.models.db_connect import get_session

router = APIRouter(prefix='/tickets', tags=['Tickets'])

@router.get("/", response_model=List[TicketResponse])
async def get_tickets(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_session)
):
    """
    Obtiene lista de tickets
    """
    return await tickets_crud.get_tickets(db, skip=skip, limit=limit)

@router.get("/{ticket_id}", response_model=TicketDetail)
async def get_ticket_detail(
    ticket_id: int,
    db: AsyncSession = Depends(get_session)
):
    """
    Obtiene detalles completos de un ticket específico
    """
    return await tickets_crud.get_ticket_details(db, ticket_id)

@router.post("/", response_model=TicketResponse)
async def create_ticket(
    ticket: TicketCreate,
    db: AsyncSession = Depends(get_session)
):
    """
    Crea un nuevo ticket para un pago completado
    """
    return await tickets_crud.create_ticket(db, ticket)