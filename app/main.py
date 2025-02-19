from fastapi import FastAPI
from .routers import reservas
from .routers import tours
from .routers import actividades
import uvicorn
# Iniciando la clase FastAPI para poder crear los endpoints
app = FastAPI()

@app.get('/')
def mensaje_root():
    return {
        "msg": "El servidor esta funcionando."
    }

app.include_router(reservas.router)
app.include_router(tours.router)
app.include_router(actividades.router)

