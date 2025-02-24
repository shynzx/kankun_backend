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
    url_imagen_tour = Column(String, nullable=False)
    stripe_product_id = Column(String, unique=True)  # ID de producto de Stripe
    stripe_price_id = Column(String, unique=True)    # ID de precio de Stripe
    
    # Relaciones
    servicios = relationship("Servicio", secondary=tour_servicio, back_populates="tours")
    pagos = relationship("Pago", back_populates="tour")