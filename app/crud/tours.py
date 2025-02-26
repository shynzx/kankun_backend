from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.servicios import Servicio
from app.models.tours import Tour
from app.schemas.tours import AddServicioToTour, TourCreate, TourUpdate, TourResponse, TourWithServicesResponse
from sqlalchemy.orm import selectinload
from typing import List

async def get_tour(db: AsyncSession, tour_id: int) -> Tour:
    result = await db.execute(select(Tour).options(selectinload(Tour.servicios)).filter(Tour.id_tour == tour_id))
    return result.scalars().first()

async def get_tour_with_services(db: AsyncSession, tour_id: int) -> Tour:
    result = await db.execute(select(Tour).options(selectinload(Tour.servicios)).filter(Tour.id_tour == tour_id))
    return result.scalars().first()

async def get_tours(db: AsyncSession, skip: int = 0, limit: int = 100) -> List[Tour]:
    result = await db.execute(select(Tour).options(selectinload(Tour.servicios)).offset(skip).limit(limit))
    return result.scalars().all()

async def create_tour(db: AsyncSession, tour: TourCreate) -> Tour:
    try:
        db_tour = Tour(
            nombre_tour=tour.nombre_tour,
            descripcion_tour=tour.descripcion_tour,
            costo_tour=tour.costo_tour,
            dias_tour=tour.dias_tour,
            tipo_tour=tour.tipo_tour,
            maxpersonas_tour=tour.maxpersonas_tour,
            direccion_inicio_tour=tour.direccion_inicio_tour,
            direccion_destino_tour=tour.direccion_destino_tour,
            imagen_tour=tour.imagen_tour
        )
        
        db.add(db_tour)
        await db.commit()
        await db.refresh(db_tour)
        return db_tour
        
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Error al crear el tour: {str(e)}")

async def update_tour(db: AsyncSession, tour_id: int, tour: TourUpdate) -> Tour:
    try:
        db_tour = await get_tour(db, tour_id)
        if not db_tour:
            raise HTTPException(status_code=404, detail="Tour no encontrado")
        
        update_data = tour.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_tour, key, value)
            
        await db.commit()
        await db.refresh(db_tour)
        return db_tour
    
    except HTTPException as e:
        raise e
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Error al actualizar el tour: {str(e)}")

async def delete_tour(db: AsyncSession, tour_id: int) -> bool:
    try:
        db_tour = await get_tour(db, tour_id)
        if not db_tour:
            raise HTTPException(status_code=404, detail="Tour no encontrado")
        
        await db.delete(db_tour)
        await db.commit()
        return True
    
    except HTTPException as e:
        raise e
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Error al eliminar el tour: {str(e)}")

async def add_servicio_to_tour(db: AsyncSession, tour_id: int, servicio_data: AddServicioToTour) -> Tour:
    try:
        db_tour = await get_tour(db, tour_id)
        if not db_tour:
            raise HTTPException(status_code=404, detail="Tour no encontrado")

        result = await db.execute(select(Servicio).filter(Servicio.id_servicio == servicio_data.id_servicio))
        db_servicio = result.scalars().first()

        if not db_servicio:
            raise HTTPException(status_code=404, detail="Servicio no encontrado")

        if db_servicio in db_tour.servicios:
            raise HTTPException(status_code=400, detail="El Servicio ya se encuentra en el Tour")

        db_tour.servicios.append(db_servicio)
        await db.commit()
        await db.refresh(db_tour)
        return db_tour

    except HTTPException as e:
        raise e
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Error al añadir el servicio al tour: {str(e)}")