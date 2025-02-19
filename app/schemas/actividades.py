from pydantic import BaseModel, Field
from typing import Optional, List

class actividad_base(BaseModel):
    nombre_servicio: str = Field(..., max_length=255)
    descripcion_servicio: str
    costo_servicio: float
    direccion_servicio: str = Field(..., max_length=255)
    alimentos_servicio: List[str]  # Matches PostgreSQL ARRAY
    horario_servicio: str = Field(..., max_length=255)
    imagen_servicio: str = Field(..., max_length=255)
    restricciones_servicio: Optional[str] = None

class actividad_crear(actividad_base):
    pass  # Se usa para crear actividades, no contiene ID

class actividad_respuesta(actividad_base):
    id: int # Contiene ID

    class Config:
        from_attributes = True  # Permite la conversión a modelos de SQLAlchemy
