from fastapi import APIRouter
from app.crud import tours

router = APIRouter()

@router.get("/tours/{tour_id}")
def obtener_tours(tour_id: int):
    return {"msg": "Obtener tours"}
