from pydantic import BaseModel, Field
from typing import Optional, List

class ServicioBase(BaseModel):
    nombre_servicio: str = Field(..., max_length=255)
    descripcion_servicio: str
    costo_servicio: float
    direccion_servicio: str = Field(..., max_length=255)
    alimentos_servicio: List[str]
    horario_servicio: str = Field(..., max_length=255)
    imagen_servicio: str = Field(..., max_length=255)
    restricciones_servicio: Optional[str] = None

class ServicioCreate(ServicioBase):
    pass

class ServicioUpdate(BaseModel):
    nombre_servicio: Optional[str] = Field(None, max_length=255)
    descripcion_servicio: Optional[str] = None
    costo_servicio: Optional[float] = None
    direccion_servicio: Optional[str] = Field(None, max_length=255)
    alimentos_servicio: Optional[List[str]] = None
    horario_servicio: Optional[str] = Field(None, max_length=255)
    imagen_servicio: Optional[str] = Field(None, max_length=255)
    restricciones_servicio: Optional[str] = None

class ServicioResponse(ServicioBase):
    id_servicio: int

    class Config:
        from_attributes = True

