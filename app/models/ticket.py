from sqlalchemy import Column, Integer, Numeric, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import Base
import datetime

class Ticket(Base):
    __tablename__ = 'tickets'

    id_ticket = Column(Integer, primary_key=True, autoincrement=True)
    fecha_ticket = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)
    total_ticket = Column(Numeric(10, 2), nullable=False)

    # Relación 1:1 con Pago
    pago = relationship("Pago", uselist=False, back_populates="ticket")