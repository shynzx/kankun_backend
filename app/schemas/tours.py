from pydantic import BaseModel
from typing import Optional

class esquema_tour(BaseModel):
    id: Optional[int] = None
    nombre_tour: str
    descripcion_tour: str
    costo_tour: float
    dias_tour: int
    tipo_tour: str
    max_personas_tour: int
    direccion_inicio_tour: str
    direccion_destino_tour: str

