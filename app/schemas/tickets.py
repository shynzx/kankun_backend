from pydantic import BaseModel
from datetime import datetime
from decimal import Decimal
from typing import Optional

class TicketBase(BaseModel):
    id_pago: int

class TicketCreate(TicketBase):
    pass

class TicketResponse(TicketBase):
    id_ticket: int
    fecha_ticket: datetime
    total_ticket: Decimal

    class Config:
        from_attributes = True

class PagoInfo(BaseModel):
    id_pago: int
    metodo_pago: str
    estado_pago: str
    fecha_pago: datetime

class TourInfo(BaseModel):
    nombre_tour: str
    tipo_tour: str
    dias_tour: int
    direccion_inicio: str
    direccion_destino: str

class ClienteInfo(BaseModel):
    usuario: str
    correo: str
    telefono: str

class TicketInfo(BaseModel):
    id_ticket: int
    fecha_ticket: datetime
    total_ticket: Decimal

class TicketDetail(BaseModel):
    ticket_info: TicketInfo
    pago_info: PagoInfo
    tour_info: TourInfo
    cliente_info: ClienteInfo

    class Config:
        from_attributes = True