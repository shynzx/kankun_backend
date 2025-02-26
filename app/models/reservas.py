from sqlalchemy import Column, Integer, String, Numeric, ForeignKey, Enum
from sqlalchemy.orm import relationship
from app.models.base import Base
import enum

class EstadoReserva(enum.Enum):
    ACTIVO = "activo"
    PENDIENTE = "pendiente"
    CANCELADO = "cancelado"

class Reserva(Base):
    __tablename__ = 'reservas'
    __table_args__ = {'extend_existing': True}
    
    id_reserva = Column(Integer, primary_key=True, autoincrement=True)
    id_usuario = Column(Integer, ForeignKey('usuarios.id_usuario'), nullable=False)
    id_tour = Column(Integer, ForeignKey('tours.id_tour'), nullable=False)
    costo_reserva = Column(Numeric(10, 2), nullable=False)
    estado = Column(Enum(EstadoReserva), nullable=False)
    stripe_product_id = Column(String, unique=True)
    stripe_price_id = Column(String, unique=True)

    # Add relationships
    usuario = relationship("Usuario", back_populates="reservas")
    tour = relationship("Tour", back_populates="reservas")