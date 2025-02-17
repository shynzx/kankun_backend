from fastapi import APIRouter

router = APIRouter()

@router.get("/reservas")
def obtener_reservas():
    return "reservas"

# Ejemplo de ruteo