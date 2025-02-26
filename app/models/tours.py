from sqlalchemy import Column, Integer, String, Numeric
from sqlalchemy.orm import relationship
from app.models.base import Base
from app.models.tour_servicio import tour_servicio

class Tour(Base):
    __tablename__ = 'tours'
    
    id_tour = Column(Integer, primary_key=True, autoincrement=True)
    nombre_tour = Column(String, nullable=False)
    descripcion_tour = Column(String, nullable=True)
    costo_tour = Column(Numeric(10, 2), nullable=False)
    dias_tour = Column(Integer, nullable=False)
    tipo_tour = Column(String, nullable=False)
    maxpersonas_tour = Column(Integer, nullable=False)
    direccion_inicio_tour = Column(String, nullable=False)
    direccion_destino_tour = Column(String, nullable=False)
    imagen_tour = Column(String, nullable=True, default="https://ralfvanveen.com/wp-content/uploads/2021/06/Placeholder-_-Glossary.svg")
    
    # Relationships
    servicios = relationship("Servicio", secondary=tour_servicio, back_populates="tours")
    pagos = relationship("Pago", back_populates="tour")
    reservas = relationship("Reserva", back_populates="tour")