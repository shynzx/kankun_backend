from sqlalchemy import Table, Column, Integer, ForeignKey
from app.models.base import Base

tour_servicio = Table(
    'tour_servicio',
    Base.metadata,
    Column('id_servicio_detalles', Integer, primary_key=True, autoincrement=True),
    Column('id_tour', Integer, ForeignKey('tours.id_tour'), nullable=False),
    Column('id_servicio', Integer, ForeignKey('servicios.id_servicio'), nullable=False)
)