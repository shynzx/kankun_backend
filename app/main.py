from fastapi import FastAPI
from .routers import reservas
from .routers import tours
from .routers import actividades
from .routers import auth
from .routers import usuarios
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
app.include_router(auth.router)
app.include_router(usuarios.router)

