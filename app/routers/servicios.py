from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.crud import servicios as servicios_crud
from app.schemas.servicios import ServicioCreate, ServicioResponse, ServicioUpdate
from app.models.db_connect import get_session
from app.crud.auth import get_current_active_user, RoleChecker

router = APIRouter(prefix='/servicios', tags=['Servicios'])

@router.get("/", response_model=List[ServicioResponse])
async def get_servicios(
    skip: int = 0, 
    limit: int = 100, 
    db: AsyncSession = Depends(get_session),
):
    servicios = await servicios_crud.get_servicios(db, skip=skip, limit=limit)
    return servicios

@router.get("/{servicio_id}", response_model=ServicioResponse)
async def get_servicio(
    servicio_id: int, 
    db: AsyncSession = Depends(get_session),
):
    servicio = await servicios_crud.get_servicio(db, servicio_id)
    if servicio is None:
        raise HTTPException(status_code=404, detail="Servicio no encontrado")
    return servicio

@router.post("/", response_model=ServicioResponse)
async def create_servicio(
    servicio: ServicioCreate, 
    db: AsyncSession = Depends(get_session),

):
    return await servicios_crud.create_servicio(db, servicio)

@router.put("/{servicio_id}", response_model=ServicioResponse)
async def update_servicio(
    servicio_id: int, 
    servicio: ServicioUpdate, 
    db: AsyncSession = Depends(get_session),

):
    updated_servicio = await servicios_crud.update_servicio(db, servicio_id, servicio)
    if updated_servicio is None:
        raise HTTPException(status_code=404, detail="Servicio no encontrado")
    return updated_servicio

@router.delete("/{servicio_id}")
async def delete_servicio(
    servicio_id: int, 
    db: AsyncSession = Depends(get_session),

):
    success = await servicios_crud.delete_servicio(db, servicio_id)
    if not success:
        raise HTTPException(status_code=404, detail="Servicio no encontrado")
    return {"message": "Servicio eliminado correctamente"}

