from pydantic import BaseModel, EmailStr
from typing import Optional

class nuevo_usuario(BaseModel):
    nombre_usuario: str
    correo_usuario: str
    telefono_usuario: str
    password_usuario: str
    rol_usuario: str
    region_usuario: str

class leer_usuario(BaseModel):
    id: int

class modificar_usuario(BaseModel):
    nombre_usuario: Optional[str] = None
    correo_usuario: Optional[EmailStr] = None
    telefono_usuario: Optional[str] = None
    password_usuario: Optional[str] = None
    rol_usuario: Optional[str] = None
    region_usuario: Optional[str] = None