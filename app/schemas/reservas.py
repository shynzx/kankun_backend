from pydantic import BaseModel
from decimal import Decimal
from typing import Optional

class ReservaBase(BaseModel):
    id_usuario: int
    id_pago: int
    id_tour: int
    costo_reserva: Decimal
    estatus: str

class ReservaCreate(ReservaBase):
    pass

class ReservaUpdate(BaseModel):
    id_usuario: Optional[int] = None
    id_pago: Optional[int] = None
    id_tour: Optional[int] = None
    costo_reserva: Optional[Decimal] = None
    estatus: Optional[str] = None

class ReservaRead(ReservaBase):
    id_reserva: int

    class Config:
        orm_mode = True
