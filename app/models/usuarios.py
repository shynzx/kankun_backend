from sqlalchemy import Column, Integer, String
from app.models.base import Base

class Usuario(Base):
    __tablename__ = 'usuarios'
    id_usuario = Column(Integer, primary_key=True, index=True)
    nombre_usuario = Column(String, nullable=False)
    correo_usuario = Column(String, unique=True, nullable=False)
    telefono_usuario = Column(String, nullable=False)
    password_usuario = Column(String, nullable=False)
    rol_usuario = Column(String, nullable=False)
    region_usuario = Column(String, nullable=False)
