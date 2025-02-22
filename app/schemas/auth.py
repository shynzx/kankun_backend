from pydantic import BaseModel, Field

class Login(BaseModel):
   correo: str = Field(description="Correo requerido para buscar el usuario en la base de datos")
   contraseña: str = Field(description="Contraseña del usuario")

class Token(BaseModel):
  access_token: str | None = Field(description="Token para almacenar la informacion de la sesión")
  refresh_token: str | None = Field(description="Token para refrescar")

class auth_response(Token):
    pass