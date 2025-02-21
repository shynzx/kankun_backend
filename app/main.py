from fastapi import FastAPI
from .routers import reservas
from .routers import tours
from .routers import auth
from .routers import usuarios
from .routers import servicios
from .routers import reservas
from .routers import payments

from fastapi.middleware.cors import CORSMiddleware

import uvicorn
# Iniciando la clase FastAPI para poder crear los endpoints
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Ajusta según tu frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.get('/')
def mensaje_root():
    return {
        "msg": "El servidor esta funcionando."
    }
app.include_router(reservas.router)
app.include_router(tours.router)
app.include_router(auth.router)
app.include_router(usuarios.router)
app.include_router(servicios.router)
app.include_router(reservas.router)
app.include_router(payments.router)
