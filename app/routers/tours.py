from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession  
from typing import List
from app.schemas.tours import *
from app.models.db_connect import get_session  
from app.crud.tours import *

router = APIRouter(prefix='/tours', tags=['Tours'])

@router.get("/", response_model=List[TourResponse])
async def get_tours_route(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_session)):
    tours = await get_tours(db, skip=skip, limit=limit)
    return [TourResponse(
        **tour.__dict__,
        servicio_ids=[servicio.id_servicio for servicio in tour.servicios]
    ) for tour in tours]

@router.get("/{tour_id}", response_model=TourResponse)
async def get_tour_route(tour_id: int, db: AsyncSession = Depends(get_session)):
    tour = await get_tour(db, tour_id)
    if tour is None:
        raise HTTPException(status_code=404, detail="Tour no encontrado")
    return TourResponse(
        **tour.__dict__,
        servicio_ids=[servicio.id_servicio for servicio in tour.servicios]
    )

@router.get("/{tour_id}/with-services", response_model=TourWithServicesResponse)
async def get_tour_with_services_route(tour_id: int, db: AsyncSession = Depends(get_session)):
    tour = await get_tour_with_services(db, tour_id)
    if tour is None:
        raise HTTPException(status_code=404, detail="Tour no encontrado")
    return TourWithServicesResponse(
        **tour.__dict__,
        servicio_ids=[servicio.id_servicio for servicio in tour.servicios],
    )

@router.post("/", response_model=TourResponse)
async def create_tour_route(tour: TourCreate, db: AsyncSession = Depends(get_session)):
    return await create_tour(db, tour)  

@router.put("/{tour_id}", response_model=TourResponse)
async def update_tour_route(tour_id: int, tour: TourUpdate, db: AsyncSession = Depends(get_session)):
    updated_tour = await update_tour(db, tour_id, tour) 
    if updated_tour is None:
        raise HTTPException(status_code=404, detail="Tour no encontrado")
    return updated_tour

@router.delete("/{tour_id}")
async def delete_tour_route(tour_id: int, db: AsyncSession = Depends(get_session)):
    success = await delete_tour(db, tour_id)  
    if not success:
        raise HTTPException(status_code=404, detail="Tour no encontrado")
    return {"message": "Tour eliminado correctamente"}

@router.post("/{tour_id}/servicios", response_model=TourResponse)
async def add_servicio_to_tour_router(tour_id: int, servicio_data: AddServicioToTour, db: AsyncSession = Depends(get_session)):
    try:
        updated_tour = await add_servicio_to_tour(db, tour_id, servicio_data)
        return updated_tour
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Hubo un error: {str(e)}")