from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.auth import create_token, authenticate_user, RoleChecker, get_current_user
from app.models.usuarios import Usuario
from app.schemas.usuarios import Token
from app.models.db_connect import get_session
from pydantic import BaseModel

ACCESS_TOKEN_EXPIRE_MINUTES = 20
REFRESH_TOKEN_EXPIRE_MINUTES = 120

router = APIRouter()

refresh_tokens = []

@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: Annotated[AsyncSession, Depends(get_session)],
):
    user = await authenticate_user(session, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    refresh_token_expires = timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)

    access_token = create_token(data={"sub": user.correo_usuario, "role": user.rol_usuario}, expires_delta=access_token_expires)
    refresh_token = create_token(data={"sub": user.correo_usuario, "role": user.rol_usuario}, expires_delta=refresh_token_expires)
    
    refresh_tokens.append(refresh_token)
    return Token(access_token=access_token, refresh_token=refresh_token)

@router.post("/refresh", response_model=Token)
async def refresh_access_token(token_data: Annotated[tuple[Usuario, str], Depends(get_current_user)]):
    user, token = token_data
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    refresh_token_expires = timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)

    access_token = create_token(data={"sub": user.correo_usuario, "role": user.rol_usuario}, expires_delta=access_token_expires)
    refresh_token = create_token(data={"sub": user.correo_usuario, "role": user.rol_usuario}, expires_delta=refresh_token_expires)

    refresh_tokens.remove(token)
    refresh_tokens.append(refresh_token)
    return Token(access_token=access_token, refresh_token=refresh_token)