from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.crud import tours as tours_crud
from app.schemas.tours import TourCreate, TourResponse, TourUpdate
from app.models.db_connect import get_session

#from app.auth import get_current_active_user, RoleChecker
#from app.auth import get_current_active_user, RoleChecker

router = APIRouter(prefix='/tours', tags=['Tours'])

#allow_create_tour = RoleChecker(["admin"])
#allow_modify_tour = RoleChecker(["admin"])

@router.get("/", response_model=List[TourResponse])
async def get_tours(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_session),

    #current_user: dict = Depends(get_current_active_user)
):
    tours = tours_crud.get_tours(db, skip=skip, limit=limit)
    return tours

@router.get("/{tour_id}", response_model=TourResponse)
async def get_tour(
    tour_id: int, 
    db: Session = Depends(get_session),
   # current_user: dict = Depends(get_current_active_user)
):
    tour = tours_crud.get_tour(db, tour_id)
    if tour is None:
        raise HTTPException(status_code=404, detail="Tour no encontrado")
    return tour

@router.post("/", response_model=TourResponse)
async def create_tour(
    tour: TourCreate, 
    db: Session = Depends(get_session),
    #current_user: dict = Depends(allow_create_tour)
    #current_user: dict = Depends(allow_create_tour)

):
    return tours_crud.create_tour(db, tour)

@router.put("/{tour_id}", response_model=TourResponse)
async def update_tour(
    tour_id: int, 
    tour: TourUpdate, 
    db: Session = Depends(get_session),
    #current_user: dict = Depends(allow_modify_tour)
    #current_user: dict = Depends(allow_modify_tour)
):
    updated_tour = tours_crud.update_tour(db, tour_id, tour)
    if updated_tour is None:
        raise HTTPException(status_code=404, detail="Tour no encontrado")
    return updated_tour

@router.delete("/{tour_id}")
async def delete_tour(
    tour_id: int, 
    db: Session = Depends(get_session),
    #current_user: dict = Depends(allow_modify_tour)
):
    success = tours_crud.delete_tour(db, tour_id)
    if not success:
        raise HTTPException(status_code=404, detail="Tour no encontrado")
    return {"message": "Tour eliminado correctamente"}

