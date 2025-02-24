from pydantic import BaseModel, field_validator
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
    
class IngresosResponse(BaseModel):
    ingresos_totales: float

    @field_validator("ingresos_totales")
    @classmethod
    def validar_ingresos_no_negativos(cls, v):
        if v < 0:
            raise ValueError("Los ingresos no pueden ser negativos")
        return v