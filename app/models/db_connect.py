import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from app.models.base import Base
from dotenv import load_dotenv
from app.models.usuarios import Usuario
from app.models.pagos import Pago
from app.models.reservas import Reserva
from app.models.servicios import Servicio
from app.models.ticket import Ticket
from app.models.tour_servicio import tour_servicio
from app.models.tours import Tour

# Cargar variables de entorno
load_dotenv()

# Configuración de la base de datos
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "KanKunDB")

# Crear conexión con la base de datos
DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:asteroide-08@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_async_engine(DATABASE_URL, echo=True)

# Crear sesión asíncrona
SessionLocal = async_sessionmaker(bind=engine, autoflush=False, autocommit=False, class_=AsyncSession)


# Obtener sesión
async def get_session():
    async with SessionLocal() as session:
        yield session

# Inicializar la base de datos y crear las tablas
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# Probar conexión
async def probar_conexion():
    try:
        async with engine.begin() as conn:
            print("✅ Conectado a la base de datos exitosamente!")
    except Exception as e:
        print(f"❌ Error conectando la base de datos: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    import asyncio

    async def main():
        await init_db()
        await probar_conexion()

    asyncio.run(main())
