from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import Base
from datetime import datetime

class Pago(Base):
    __tablename__ = 'pagos'

    id_pago = Column(Integer, primary_key=True, autoincrement=True)
    stripe_session_id = Column(String, unique=True, nullable=False)
    stripe_customer_id = Column(String, nullable=False)
    stripe_price_id = Column(String, nullable=False)
    metodo_pago = Column(String, nullable=False)
    iva_pago = Column(Float, nullable=False)
    estado_pago = Column(String, nullable=False)
    costo_total_pago = Column(Float, nullable=False)
    fecha_pago = Column(DateTime, default=datetime.utcnow)
    id_usuario = Column(Integer, ForeignKey('usuarios.id_usuario'), nullable=False)
    id_tour = Column(Integer, ForeignKey('tours.id_tour'), nullable=False)

    # Relaciones
    usuario = relationship("Usuario", back_populates="pagos")
    tour = relationship("Tour", back_populates="pagos")
    ticket = relationship("Ticket", back_populates="pago", uselist=False)