from sqlalchemy import Column, Integer, Numeric, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import Base
import datetime

class Ticket(Base):
    __tablename__ = 'tickets'

    id_ticket = Column(Integer, primary_key=True, autoincrement=True)
    fecha_ticket = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)
    total_ticket = Column(Numeric(10, 2), nullable=False)
    id_pago = Column(Integer, ForeignKey('pagos.id_pago'), unique=True)

    # Relación 1:1 con Pago
    pago = relationship("Pago", back_populates="ticket", uselist=False)