from pydantic import BaseModel
from decimal import Decimal
from typing import Optional

from app.models.reservas import EstadoReserva

class ReservaBase(BaseModel):
    id_usuario: int
    id_tour: int
    costo_reserva: Decimal
    estado: EstadoReserva

class ReservaCreate(ReservaBase):
    pass

class ReservaUpdate(BaseModel):
    id_usuario: Optional[int] = None
    id_tour: Optional[int] = None
    costo_reserva: Optional[Decimal] = None
    estado: Optional[EstadoReserva] = None

class ReservaResponse(ReservaBase):
    id_reserva: int
    stripe_product_id: Optional[str] = None
    stripe_price_id: Optional[str] = None

    class Config:
        from_attributes = True