# CRUD DE ACTIVIDADES

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from app.models.db_connect import 

router = APIRouter(prefix="/servicios", tags=["Servicios"])

@router.post("/", response_model=ServicioRead)
async def create_servicio(servicio: ServicioCreate, session: AsyncSession = Depends(get_session)):
    existing_service = await session.execute(select(Servicio).where(Servicio.nombre_servicio == servicio.nombre_servicio))
    if existing_service.scalar():
        raise HTTPException(status_code=400, detail="El servicio ya existe.")

    nuevo_servicio = Servicio(**servicio.model_dump())  
    session.add(nuevo_servicio)
    await session.commit()
    await session.refresh(nuevo_servicio)
    return nuevo_servicio

@router.get("/", response_model=list[ServicioRead])
async def get_servicios(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Servicio))
    return result.scalars().all()

@router.get("/{servicio_id}", response_model=ServicioRead)
async def get_servicio(servicio_id: int, session: AsyncSession = Depends(get_session)):
    servicio = await session.get(Servicio, servicio_id)
    if not servicio:
        raise HTTPException(status_code=404, detail="Servicio no fue encontrado")
    return servicio

@router.put("/{servicio_id}", response_model=ServicioRead)
async def update_servicio(servicio_id: int, update_data: ServicioUpdate, session: AsyncSession = Depends(get_session)):
    servicio = await session.get(Servicio, servicio_id)
    if not servicio:
        raise HTTPException(status_code=404, detail="Servicio no fue encontrado")
    
    update_data_dict = update_data.model_dump(exclude_unset=True)
    for key, value in update_data_dict.items():
        setattr(servicio, key, value)

    session.add(servicio)
    await session.commit()
    await session.refresh(servicio)
    return servicio

@router.delete("/{servicio_id}")
async def delete_servicio(servicio_id: int, session: AsyncSession = Depends(get_session)):
    servicio = await session.get(Servicio, servicio_id)
    if not servicio:
        raise HTTPException(status_code=404, detail="Servicio no fue encontrado")
    
    await session.delete(servicio)
    await session.commit()
    return {"message": "Servicio eliminado exitosamente"}

