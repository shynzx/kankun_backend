from pydantic import BaseModel
from typing import Dict

#class reservaResponse(BaseModel):
#    reservasOrdenadas: List[int]
    
class cancelacionResponse(BaseModel):
    reservasCanceladas: int
    reservasCanceladasPorcentaje: float
    reservasTotal: int
    
class masReservadoResponse(BaseModel):
    tour_id: int
    tour_name: str
    total_reservations: int