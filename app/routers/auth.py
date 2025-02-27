from datetime import timedelta
import os
from typing import Annotated
from jose import jwt

from sqlalchemy.future import select
from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import requests
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.auth import create_token, authenticate_user, RoleChecker, get_current_user
from app.models.usuarios import RolUsuario, Usuario
from app.schemas.auth import Login, Token, auth_response
from app.models.db_connect import get_session

ACCESS_TOKEN_EXPIRE_MINUTES = 60
REFRESH_TOKEN_EXPIRE_MINUTES = 120
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
GOOGLE_REDIRECT_URI = os.getenv("GOOGLE_REDIRECT_URI")

refresh_tokens = []

admin_rutas = RoleChecker([RolUsuario.admin]) #define los roles que va a aceptar el role checker
cliente_rutas = RoleChecker([RolUsuario.cliente])
ambos = RoleChecker([RolUsuario.cliente, RolUsuario.admin])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login/auth")

router = APIRouter(prefix='/login', tags=['auth'])

@router.get("/dashboard", dependencies=[Depends(admin_rutas)], summary="Endpoint RBAC de prueba")
async def admin_dashboard():
    """
    Prueba de RBAC, este endpoint solo sirve para hacer pruebas de RBAC,
    """
    return {"msg": "Bienvenido al panel de administración"}

@router.post("/auth", response_model=auth_response, summary="Crea un nuevo token",response_description="Los tokens con la información de la sesión",)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: Annotated[AsyncSession, Depends(get_session)],
):
    """
    Genera un nuevo token para autorizar al usuario:

    - **correo**: correo del usuario registrado
    - **contraseña**: contraseña del usuario registrado
    
    """
    user = await authenticate_user(session, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    refresh_token_expires = timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)

    access_token = create_token(data={"sub": user.correo_usuario, "role": user.rol_usuario.value}, expires_delta=access_token_expires)
    refresh_token = create_token(data={"sub": user.correo_usuario, "role": user.rol_usuario.value}, expires_delta=refresh_token_expires)
    
    refresh_tokens.append(refresh_token)
    return auth_response(access_token=access_token, refresh_token=refresh_token)



@router.post("/refreshToken", response_model=Token, summary="Refresca la sesion")
async def refresh_access_token(token_data: Annotated[tuple[Usuario, str], Depends(get_current_user)]):
    user, token = token_data
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    refresh_token_expires = timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)

    access_token = create_token(data={"sub": user.correo_usuario, "role": user.rol_usuario}, expires_delta=access_token_expires)
    refresh_token = create_token(data={"sub": user.correo_usuario, "role": user.rol_usuario}, expires_delta=refresh_token_expires)
    """
    no implementado(solo refresca la sesion)
    """
    refresh_tokens.remove(token)
    refresh_tokens.append(refresh_token)
    return Token(access_token=access_token, refresh_token=refresh_token)

#-----google_auth-----

@router.get("/login_google", summary="Regresa una url de redireccionamiento a google/auth")
async def login_google():
    """
    regresa la url para el registro con google
    """
    return {
        "url": f"https://accounts.google.com/o/oauth2/auth?response_type=code&client_id={GOOGLE_CLIENT_ID}&redirect_uri={GOOGLE_REDIRECT_URI}&scope=openid%20profile%20email&access_type=offline"
    }

@router.get("/auth/google",summary="El usuario podra seleccionar su cuenta y poderse registrar en la aplicacion")
async def auth_google(code: str,db: AsyncSession = Depends(get_session)):
    """
    NO USAR: esta ruta es implementada para que la api de google pueda regresar el token con la informacion de la sesion
    """
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

    result = await db.execute(select(Usuario).where(Usuario.correo_usuario == email))
    usuario = result.scalars().first()

    if not usuario:
        nuevo_usuario = Usuario(
            nombre_usuario=nombre,
            correo_usuario=email,
            rol_usuario=RolUsuario.cliente,
            region_usuario="default"
        )
        db.add(nuevo_usuario)
        await db.commit()
        await db.refresh(nuevo_usuario)
        usuario = nuevo_usuario
    
    access_token = create_token(
        data={"sub": usuario.correo_usuario, "role": usuario.rol_usuario.value},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/token", summary="Token")
async def get_token(token: str = Depends(oauth2_scheme)):
    
    return jwt.decode(token, GOOGLE_CLIENT_SECRET, algorithms=["HS256"])