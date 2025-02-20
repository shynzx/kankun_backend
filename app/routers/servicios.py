from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.crud import servicios as servicios_crud
from app.schemas.servicios import ServicioCreate, ServicioResponse, ServicioUpdate
from app.models.db_connect import get_db
from app.auth import get_current_active_user, RoleChecker

router = APIRouter(prefix='/servicios', tags=['Servicios'])

allow_create_servicio = RoleChecker(["admin"])
allow_modify_servicio = RoleChecker(["admin"])

@router.get("/", response_model=List[ServicioResponse])
async def get_servicios(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_active_user)
):
    servicios = servicios_crud.get_servicios(db, skip=skip, limit=limit)
    return servicios

@router.get("/{servicio_id}", response_model=ServicioResponse)
async def get_servicio(
    servicio_id: int, 
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_active_user)
):
    servicio = servicios_crud.get_servicio(db, servicio_id)
    if servicio is None:
        raise HTTPException(status_code=404, detail="Servicio no encontrado")
    return servicio

@router.post("/", response_model=ServicioResponse)
async def create_servicio(
    servicio: ServicioCreate, 
    db: Session = Depends(get_db),
    current_user: dict = Depends(allow_create_servicio)
):
    return servicios_crud.create_servicio(db, servicio)

@router.put("/{servicio_id}", response_model=ServicioResponse)
async def update_servicio(
    servicio_id: int, 
    servicio: ServicioUpdate, 
    db: Session = Depends(get_db),
    current_user: dict = Depends(allow_modify_servicio)
):
    updated_servicio = servicios_crud.update_servicio(db, servicio_id, servicio)
    if updated_servicio is None:
        raise HTTPException(status_code=404, detail="Servicio no encontrado")
    return updated_servicio

@router.delete("/{servicio_id}")
async def delete_servicio(
    servicio_id: int, 
    db: Session = Depends(get_db),
    current_user: dict = Depends(allow_modify_servicio)
):
    success = servicios_crud.delete_servicio(db, servicio_id)
    if not success:
        raise HTTPException(status_code=404, detail="Servicio no encontrado")
    return {"message": "Servicio eliminado correctamente"}

