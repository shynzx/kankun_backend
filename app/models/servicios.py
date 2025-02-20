from sqlalchemy import Column, Integer, String, Float, Text
from sqlalchemy.orm import relationship
from app.models.base import Base
from app.models.tour_servicio import tour_servicio
from sqlalchemy.dialects.postgresql import ARRAY

class Servicio(Base):
    __tablename__ = "servicios"

    id_servicio = Column(Integer, primary_key=True, autoincrement=True)
    nombre_servicio = Column(String(255), nullable=False)
    descripcion_servicio = Column(Text, nullable=False)
    costo_servicio = Column(Float, nullable=False)
    direccion_servicio = Column(String(255), nullable=False)
    alimentos_servicio = Column(ARRAY(String), nullable=False)  # PostgreSQL ARRAY (tipo de dato)
    horario_servicio = Column(String(255), nullable=False)
    imagen_servicio = Column(String(255), nullable=False)
    restricciones_servicio = Column(Text, nullable=True)  # C'est opcional
    # Relacion N:N con tours
    tours = relationship("Tour", secondary=tour_servicio, back_populates="servicios")