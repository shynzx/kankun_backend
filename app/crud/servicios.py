from sqlalchemy.ext.asyncio import AsyncSession 
from sqlalchemy.future import select
from app.models.servicios import Servicio
from app.schemas.servicios import ServicioCreate, ServicioUpdate
from fastapi import APIRouter, Depends
from typing import List, Optional

router = APIRouter()

@router.get("/servicios/{servicio_id}", response_model=Optional[Servicio], summary="Obtener un servicio por ID")
async def get_servicio(db: AsyncSession, servicio_id: int):
    """
    Obtiene un servicio específico por su ID.
    
    - *servicio_id*: ID único del servicio a recuperar.
    """
    result = await db.execute(select(Servicio).filter(Servicio.id_servicio == servicio_id))
    return result.scalar_one_or_none()

@router.get("/servicios/", response_model=List[Servicio], summary="Obtener lista de servicios")
async def get_servicios(db: AsyncSession, skip: int = 0, limit: int = 100):
    """
    Recupera una lista paginada de servicios.
    
    - *skip*: Número de registros a omitir (paginación).
    - *limit*: Número máximo de registros a devolver.
    """
    result = await db.execute(select(Servicio).offset(skip).limit(limit))
    return result.scalars().all()

@router.post("/servicios/", response_model=Servicio, summary="Crear un nuevo servicio")
async def create_servicio(db: AsyncSession, servicio: ServicioCreate):
    """
    Crea un nuevo servicio en la base de datos.
    
    - *servicio*: Datos del nuevo servicio a registrar.
    """
    db_servicio = Servicio(**servicio.dict())
    db.add(db_servicio)
    await db.commit()
    await db.refresh(db_servicio)
    return db_servicio

@router.put("/servicios/{servicio_id}", response_model=Optional[Servicio], summary="Actualizar un servicio")
async def update_servicio(db: AsyncSession, servicio_id: int, servicio: ServicioUpdate):
    """
    Actualiza un servicio existente por su ID.
    
    - *servicio_id*: ID único del servicio a actualizar.
    - *servicio*: Datos a modificar.
    """
    db_servicio = await get_servicio(db, servicio_id)
    if db_servicio:
        update_data = servicio.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_servicio, key, value)
        await db.commit()
        await db.refresh(db_servicio)
    return db_servicio

@router.delete("/servicios/{servicio_id}", response_model=bool, summary="Eliminar un servicio")
async def delete_servicio(db: AsyncSession, servicio_id: int):
    """
    Elimina un servicio de la base de datos por su ID.
    
    - *servicio_id*: ID único del servicio a eliminar.
    """
    db_servicio = await get_servicio(db, servicio_id)
    if db_servicio:
        await db.delete(db_servicio)
        await db.commit()
        return True
    return False