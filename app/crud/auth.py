from fastapi.security import OAuth2PasswordBearer 
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone
from typing import Annotated
from fastapi import Depends, HTTPException, status

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models.usuarios import Usuario
from app.models.db_connect import get_session

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = "hdhfh5jdnb7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"

async def get_user(session: AsyncSession, correo_usuario: str):
    stmt = select(Usuario).where(Usuario.correo_usuario == correo_usuario)  # Usar filter_by para atributos de clase
    try:
        result = await session.execute(stmt)  # Ejecutar la consulta
    except:
        raise HTTPException(status_code=404, detail="el ususario no existe en la base de datos")
    return result.scalars().first()


async def authenticate_user(session: AsyncSession, correo_usuario: str, password: str):
    user = await get_user(session, correo_usuario)
    if not user:
        return False
    if not pwd_context.verify(password, user.password_usuario):
        return False
    return user

def create_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], session: AsyncSession = Depends(get_session)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        correo_usuario: str = payload.get("sub")
        if correo_usuario is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = await get_user(session, correo_usuario=correo_usuario)
    if user is None:
        raise credentials_exception
    return user

async def get_current_active_user(current_user: Annotated[Usuario, Depends(get_current_user)]):
    return current_user

class RoleChecker:
    def __init__(self, allowed_roles):
        self.allowed_roles = allowed_roles

    def __call__(self, user: Annotated[Usuario, Depends(get_current_active_user)]):
        if user.rol_usuario in self.allowed_roles:
            return True
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="You don't have enough permissions"
        )
