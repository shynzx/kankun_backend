from fastapi import APIRouter
#from app.crud.reservas import 

router = APIRouter()

@router.get("/actividades/{id_actividad}")
async def obtener_actividades(id_actividad: int):
    return {"msg": "Obtener actividades"}


