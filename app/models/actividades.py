from sqlalchemy import Column, Integer, String, Float, Text
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.dialects.postgresql import ARRAY

class Base(DeclarativeBase):
    pass

class Actividad(Base):
    __tablename__ = "actividad"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre_servicio = Column(String(255), nullable=False)
    descripcion_servicio = Column(Text, nullable=False)
    costo_servicio = Column(Float, nullable=False)
    direccion_servicio = Column(String(255), nullable=False)
    alimentos_servicio = Column(ARRAY(String), nullable=False)  # PostgreSQL ARRAY (tipo de dato)
    horario_servicio = Column(String(255), nullable=False)
    imagen_servicio = Column(String(255), nullable=False)
    restricciones_servicio = Column(Text, nullable=True)  # C'est opcional
