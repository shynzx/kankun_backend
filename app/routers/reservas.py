from fastapi import APIRouter

router = APIRouter()

@router.get("/reservas")
def obtener_reservas():
    return {"msg": "reservas"}

# Ejemplo de ruteo