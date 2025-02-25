from datetime import timedelta
from typing import Annotated
from jose import jwt

from sqlalchemy.future import select
from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
import requests
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.auth import create_token, authenticate_user, RoleChecker, get_current_user
from app.models.usuarios import RolUsuario, Usuario
from app.schemas.auth import Login, Token, auth_response
from app.models.db_connect import get_session
from pydantic import BaseModel

ACCESS_TOKEN_EXPIRE_MINUTES = 20
REFRESH_TOKEN_EXPIRE_MINUTES = 120
GOOGLE_CLIENT_ID = "aqui va el id"
GOOGLE_CLIENT_SECRET = "aqui van los secrets"
GOOGLE_REDIRECT_URI = "aqui va la uri"

refresh_tokens = []

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

router = APIRouter(prefix='/login', tags=['auth'])

@router.post("/auth", response_model=auth_response, summary="Crea un nuevo token",response_description="Los tokens con la información de la sesión",)
async def login_for_access_token(
    form_data: Annotated[Login, Query()],
    session: Annotated[AsyncSession, Depends(get_session)],
):
    """
    Genera un nuevo token para autorizar al usuario:

    - **correo**: correo del usuario registrado
    - **contraseña**: contraseña del usuario registrado
    
    """
    user = await authenticate_user(session, form_data.correo, form_data.contraseña)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    refresh_token_expires = timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)

    access_token = create_token(data={"sub": user.correo_usuario, "role": user.rol_usuario.value}, expires_delta=access_token_expires)
    refresh_token = create_token(data={"sub": user.correo_usuario, "role": user.rol_usuario.value}, expires_delta=refresh_token_expires)
    
    refresh_tokens.append(refresh_token)
    return auth_response(access_token=access_token, refresh_token=refresh_token)

@router.post("/refreshToken", response_model=Token)
async def refresh_access_token(token_data: Annotated[tuple[Usuario, str], Depends(get_current_user)]):
    user, token = token_data
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    refresh_token_expires = timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)

    access_token = create_token(data={"sub": user.correo_usuario, "role": user.rol_usuario}, expires_delta=access_token_expires)
    refresh_token = create_token(data={"sub": user.correo_usuario, "role": user.rol_usuario}, expires_delta=refresh_token_expires)

    refresh_tokens.remove(token)
    refresh_tokens.append(refresh_token)
    return Token(access_token=access_token, refresh_token=refresh_token)

#-----google_auth-----

@router.get("/login_google")
async def login_google():
    return {
        "url": f"https://accounts.google.com/o/oauth2/auth?response_type=code&client_id={GOOGLE_CLIENT_ID}&redirect_uri={GOOGLE_REDIRECT_URI}&scope=openid%20profile%20email&access_type=offline"
    }

@router.get("/auth/google")
async def auth_google(code: str,db: AsyncSession = Depends(get_session)):
    token_url = "https://accounts.google.com/o/oauth2/token"
    data = {
        "code": code,
        "client_id": GOOGLE_CLIENT_ID,
        "client_secret": GOOGLE_CLIENT_SECRET,
        "redirect_uri": GOOGLE_REDIRECT_URI,
        "grant_type": "authorization_code",
    }
    response = requests.post(token_url, data=data)
    token_data = response.json()
    access_token = token_data.get("access_token")

    if not access_token:
        return {"error": "No se pudo obtener el access_token", "response": token_data}

    user_info_response = requests.get(
        "https://www.googleapis.com/oauth2/v1/userinfo",
        headers={"Authorization": f"Bearer {access_token}"}
    )

    if user_info_response.status_code != 200:
        return {"error": "Error al obtener la información del usuario", "details": user_info_response.json()}

    user_data = user_info_response.json()
    email = user_data["email"]
    nombre = user_data["name"]

    # Verificar si el usuario ya existe
    result = await db.execute(select(Usuario).where(Usuario.correo_usuario == email))
    usuario = result.scalars().first()

    if not usuario:
        # Crear usuario con rol "cliente" por defecto
        nuevo_usuario = Usuario(
            nombre_usuario=nombre,
            correo_usuario=email,
            rol_usuario=RolUsuario.cliente,  # Asignar correctamente el Enum
            region_usuario="default"
        )
        db.add(nuevo_usuario)
        await db.commit()
        await db.refresh(nuevo_usuario)
        usuario = nuevo_usuario

    return {"usuario": usuario.correo_usuario, "rol": usuario.rol_usuario.value}

@router.get("/token")
async def get_token(token: str = Depends(oauth2_scheme)):
    return jwt.decode(token, GOOGLE_CLIENT_SECRET, algorithms=["HS256"])