from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession  
from typing import List
from app.schemas.tours import *
from app.models.db_connect import get_session  
from app.crud.tours import *

router = APIRouter(prefix='/tours', tags=['Tours'])

@router.get("/", response_model=List[TourResponse], responses={
    200: {'description': 'Lista de tours obtenida exitosamente'},
    500: {'description': 'Error interno'}
})
async def get_tours_route(skip: int = 0, limit: int = 100):
    """
    Obtener la lista de tours.
    
    - **skip**: Número de registros a omitir.
    - **limit**: Número máximo de registros a retornar.
    """
    tours = await get_tours(skip=skip, limit=limit)
    return [TourResponse(
        **tour.__dict__,
        servicio_ids=[servicio.id_servicio for servicio in tour.servicios]
    ) for tour in tours]

@router.get("/{tour_id}", response_model=TourResponse, responses={
    200: {'description': 'Tour encontrado exitosamente'},
    404: {'description': 'Tour no encontrado'},
    500: {'description': 'Error interno'}
})
async def get_tour_route(tour_id: int):
    """
    Obtener un tour por su ID.
    
    - **tour_id**: ID del tour a buscar.
    """
    tour = await get_tour(tour_id)
    if tour is None:
        raise HTTPException(status_code=404, detail="Tour no encontrado")
    return TourResponse(
        **tour.__dict__,
        servicio_ids=[servicio.id_servicio for servicio in tour.servicios]
    )

@router.get("/{tour_id}/with-services", response_model=TourWithServicesResponse)
async def get_tour_with_services_route(tour_id: int):
    """
    Obtener un tour con sus servicios asociados.
    
    - **tour_id**: ID del tour a buscar.
    """
    tour = await get_tour_with_services(tour_id)
    if tour is None:
        raise HTTPException(status_code=404, detail="Tour no encontrado")
    return TourWithServicesResponse(
        **tour.__dict__,
        servicio_ids=[servicio.id_servicio for servicio in tour.servicios],
    )

@router.post("/", response_model=TourResponse)
async def create_tour_route(tour: TourCreate):
    """
    Crear un nuevo tour.
    
    - **tour**: Datos del tour a crear.
    """
    return await create_tour(tour)  

@router.put("/{tour_id}", response_model=TourResponse)
async def update_tour_route(tour_id: int, tour: TourUpdate):
    """
    Actualizar un tour existente.
    
    - **tour_id**: ID del tour a actualizar.
    - **tour**: Datos a modificar.
    """
    updated_tour = await update_tour(tour_id, tour) 
    if updated_tour is None:
        raise HTTPException(status_code=404, detail="Tour no encontrado")
    return updated_tour

@router.delete("/{tour_id}")
async def delete_tour_route(tour_id: int):
    """
    Eliminar un tour por su ID.
    
    - **tour_id**: ID del tour a eliminar.
    """
    success = await delete_tour(tour_id)  
    if not success:
        raise HTTPException(status_code=404, detail="Tour no encontrado")
    return {"message": "Tour eliminado correctamente"}

@router.post("/{tour_id}/servicios", response_model=TourResponse)
async def add_servicio_to_tour_router(tour_id: int, servicio_data: AddServicioToTour):
    """
    Agregar un servicio a un tour.
    
    - **tour_id**: ID del tour.
    - **servicio_data**: Datos del servicio a agregar.
    """
    try:
        updated_tour = await add_servicio_to_tour(tour_id, servicio_data)
        return updated_tour
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Hubo un error: {str(e)}")
