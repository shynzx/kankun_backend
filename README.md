Repositorio del backend del sistema de gestión de tours KanKun.

Comandos relevantes (Recordatorio de que deben tener el .venv activado):

Para activar .venv:
    En la carpeta .venv/Scripts/:

    activate

Para correr FASTAPI:
    En la carpeta /app: 
    
    fastapi dev main.py

Para iniciar la base de datos (correr el archivo db_connect.py)
    En la carpeta /root (carpeta de origen, previa a app): 
    
    py -m app.models.db_connect