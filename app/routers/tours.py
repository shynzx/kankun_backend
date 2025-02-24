from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession  
from typing import List
from app.crud import tours as tours_crud
from app.schemas.tours import TourCreate, TourResponse, TourUpdate
from app.models.db_connect import get_session  

router = APIRouter(prefix='/tours', tags=['Tours'])

@router.get("/", response_model=List[TourResponse])
async def get_tours(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_session)):
    tours = await tours_crud.get_tours(db, skip=skip, limit=limit)  
    return tours

@router.get("/{tour_id}", response_model=TourResponse)
async def get_tour(tour_id: int, db: AsyncSession = Depends(get_session)):
    tour = await tours_crud.get_tour(db, tour_id)  
    if tour is None:
        raise HTTPException(status_code=404, detail="Tour no encontrado")
    return tour

@router.post("/", response_model=TourResponse)
async def create_tour(tour: TourCreate, db: AsyncSession = Depends(get_session)):
    return await tours_crud.create_tour(db, tour)  

@router.put("/{tour_id}", response_model=TourResponse)
async def update_tour(tour_id: int, tour: TourUpdate, db: AsyncSession = Depends(get_session)):
    updated_tour = await tours_crud.update_tour(db, tour_id, tour) 
    if updated_tour is None:
        raise HTTPException(status_code=404, detail="Tour no encontrado")
    return updated_tour

@router.delete("/{tour_id}")
async def delete_tour(tour_id: int, db: AsyncSession = Depends(get_session)):
    success = await tours_crud.delete_tour(db, tour_id)  
    if not success:
        raise HTTPException(status_code=404, detail="Tour no encontrado")
    return {"message": "Tour eliminado correctamente"}

@router.post("/{tour_id}/servicios", response_model=TourResponse)
async def add_servicio_to_tour(tour_id: int, servicio_data: AddServicioToTour, db: AsyncSession = Depends(get_session)):
    try:
        updated_tour = await tours_crud.add_servicio_to_tour(db, tour_id, servicio_data)
        return updated_tour
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Hubo un error: {str(e)}")