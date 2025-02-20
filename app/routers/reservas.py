from sqlalchemy import Column, Integer, String, Numeric, ForeignKey
from app.models.base import Base

class Reserva(Base):
    __tablename__ = 'reservas'
    
    id_reserva = Column(Integer, primary_key=True, autoincrement=True)
    id_usuario = Column(Integer, ForeignKey('usuarios.id_usuario'), nullable=False)
    id_pago = Column(Integer, ForeignKey('pagos.id_pago'), nullable=False)
    id_tour = Column(Integer, ForeignKey('tours.id_tour'), nullable=False)
    costo_reserva = Column(Numeric(10, 2), nullable=False)
    estatus = Column(String, nullable=False)

