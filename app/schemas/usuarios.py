from pydantic import BaseModel, EmailStr
from typing import Optional

from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class UsuarioBase(BaseModel):
    nombre_usuario: str = Field(..., max_length=255)
    correo_usuario: EmailStr
    telefono_usuario: str = Field(..., max_length=20)
    rol_usuario: str = Field(..., max_length=50)
    region_usuario: str = Field(..., max_length=100)

class crear_usuario(UsuarioBase):
    password_usuario: str = Field(..., min_length=6)

class buscar_usuario(UsuarioBase):
    id_usuario: int

    class Config:
        from_attributes = True

class Token(BaseModel):
  access_token: str | None = None
  refresh_token: str | None = None

class auth_response(Token):
    correo_usuario: str