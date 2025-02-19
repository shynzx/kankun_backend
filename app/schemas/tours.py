from pydantic import BaseModel, Field
from typing import Optional

class TourBase(BaseModel):
    nombre_tour: str = Field(..., max_length=255)
    descripcion_tour: str
    costo_tour: float
    dias_tour: int
    tipo_tour: str = Field(..., max_length=100)
    max_personas_tour: int
    direccion_inicio_tour: str = Field(..., max_length=255)
    direccion_destino_tour: str = Field(..., max_length=255)

class TourCreate(TourBase):
    pass  # No contiene ID, se usa para crear nuevos tours.

class TourResponse(TourBase):
    id: int

    class Config:
        from_attributes = True  # Permite la conversión a modelos de SQLAlchemy

