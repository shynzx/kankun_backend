from pydantic import BaseModel
from typing import Optional

class esquema_actividad(BaseModel):
    id: Optional[int] = None
    nombre_servicio: str
    descripcion_servicio: str
    costo_servicio: float
    direccion_servicio: str
    alimentos_servicio: list[str]
    horario_servicio: str
    imagen_servicio: str
    restricciones_servicio: Optional[str] = None
