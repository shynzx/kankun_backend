from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.security import OAuth2PasswordRequestForm
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.auth import create_token, authenticate_user, RoleChecker, get_current_user
from app.models.usuarios import Usuario
from app.schemas.auth import Login, Token, auth_response
from app.models.db_connect import get_session
from pydantic import BaseModel

ACCESS_TOKEN_EXPIRE_MINUTES = 20
REFRESH_TOKEN_EXPIRE_MINUTES = 120

refresh_tokens = []

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
    user = await authenticate_user(session, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    refresh_token_expires = timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)

    access_token = create_token(data={"sub": user.correo_usuario, "role": user.rol_usuario}, expires_delta=access_token_expires)
    refresh_token = create_token(data={"sub": user.correo_usuario, "role": user.rol_usuario}, expires_delta=refresh_token_expires)
    
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