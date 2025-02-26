from pydantic import BaseModel, Field
from app.schemas.servicios import ServicioResponse
from typing import Optional, List
from app.schemas.servicios import ServicioResponse

class TourBase(BaseModel):
    nombre_tour: str = Field(..., max_length=255)
    descripcion_tour: str
    costo_tour: float
    dias_tour: int
    tipo_tour: str = Field(..., max_length=100)
    maxpersonas_tour: int
    imagen_tour: str = Field(None, max_length=500)
    direccion_inicio_tour: str = Field(..., max_length=255)
    direccion_destino_tour: str = Field(..., max_length=255)

class TourCreate(TourBase):
    pass

class TourUpdate(BaseModel):
    nombre_tour: Optional[str] = Field(None, max_length=255)
    descripcion_tour: Optional[str] = None
    costo_tour: Optional[float] = None
    dias_tour: Optional[int] = None
    tipo_tour: Optional[str] = Field(None, max_length=100)
    maxpersonas_tour: Optional[int] = None
    imagen_tour:Optional[str] = Field(None, max_length=500)
    direccion_inicio_tour: Optional[str] = Field(None, max_length=255)
    direccion_destino_tour: Optional[str] = Field(None, max_length=255)

class TourResponse(TourBase):
    id_tour: int
    servicio_ids: List[int] = []

    class Config:
        from_attributes = True

class TourWithServicesResponse(TourResponse):
    servicios: List['ServicioResponse'] = []

class AddServicioToTour(BaseModel):
    id_servicio: int