from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.usuarios import UsuarioCreate, UsuarioResponse
from app.crud.usuarios import create_usuario, get_usuario_by_email
from app.models.db_connect import get_session

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])

@router.post("/", response_model=UsuarioResponse, status_code=201)
async def registrar_usuario(usuario: UsuarioCreate, db: AsyncSession = Depends(get_session)):
    db_usuario = await get_usuario_by_email(db, usuario.correo_usuario)
    if db_usuario:
        raise HTTPException(status_code=400, detail="El correo ya está registrado")
    
    return await create_usuario(db, usuario)