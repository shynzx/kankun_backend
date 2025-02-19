from sqlalchemy import Column, Integer, String, Float, Text
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

class Tour(Base):
    __tablename__ = "tour"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre_tour = Column(String(255), nullable=False)
    descripcion_tour = Column(Text, nullable=False)
    costo_tour = Column(Float, nullable=False)
    dias_tour = Column(Integer, nullable=False)
    tipo_tour = Column(String(100), nullable=False)
    max_personas_tour = Column(Integer, nullable=False)
    direccion_inicio_tour = Column(String(255), nullable=False)
    direccion_destino_tour = Column(String(255), nullable=False)
