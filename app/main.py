from fastapi import FastAPI
from .routers import reservas
import uvicorn
# Iniciando la clase FastAPI para poder crear los endpoints
app = FastAPI()

@app.get('/')
def mensaje_root():
    return {
        "msg": "El servidor esta funcionando."
    }

app.include_router(reservas.router)

