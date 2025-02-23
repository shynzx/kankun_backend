from sqlalchemy import Column, Integer, String, Enum as SqlEnum
from app.models.base import Base
from sqlalchemy.orm import relationship
from enum import Enum
class RolUsuario(Enum):
    admin = "admin"
    cliente = "cliente"

class Usuario(Base):
    __tablename__ = 'usuarios'
    id_usuario = Column(Integer, primary_key=True, index=True)
    nombre_usuario = Column(String, nullable=False)
    correo_usuario = Column(String, unique=True, nullable=False)
    telefono_usuario = Column(String, nullable=False)
    password_usuario = Column(String, nullable=False)
    rol_usuario = Column(SqlEnum(RolUsuario), nullable=False)
    region_usuario = Column(String, nullable=False)
    stripe_customer_id = Column(String, unique=True)  # ID de cliente de Stripe
    
    # Relaciones
    pagos = relationship("Pago", back_populates="usuario")