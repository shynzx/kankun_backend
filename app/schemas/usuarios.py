from pydantic import BaseModel, EmailStr
from typing import Optional

from pydantic import BaseModel, EmailStr, Field
from typing import Optional

from app.models.usuarios import RolUsuario

class UsuarioBase(BaseModel):
    nombre_usuario: str = Field(..., max_length=255)
    correo_usuario: EmailStr
    telefono_usuario: str = Field(..., max_length=20)
    rol_usuario: RolUsuario = Field(default=RolUsuario.cliente)
    region_usuario: str = Field(..., max_length=100)
    

class crear_usuario(UsuarioBase):
    password_usuario: str = Field(..., min_length=6)

class buscar_usuario(UsuarioBase):
    id_usuario: int

    class Config:
        from_attributes = True

