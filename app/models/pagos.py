from sqlalchemy import Column, Integer, String, Numeric, ForeignKey
from app.models.base import Base
from sqlalchemy.orm import relationship


class Pago(Base):
    __tablename__ = 'pagos'

    id_pago = Column(Integer, primary_key=True, autoincrement=True)
    id_ticket = Column(Integer, ForeignKey('tickets.id_ticket'), unique=True, nullable=False)
    metodo_pago = Column(String, nullable=False)
    iva_pago = Column(Numeric(10, 2), nullable=False)
    estado_pago = Column(String, nullable=False)
    costo_total_pago = Column(Numeric(10, 2), nullable=False)

    # Relación 1:1 con Ticket
    ticket = relationship("Ticket", back_populates="pago")