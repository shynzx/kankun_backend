import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Database Configuration
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "KanKunDB")

# SQLAlchemy CREATE Engine
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(DATABASE_URL, echo=True)  # `echo=True` logs queries (useful for debugging)

# Session Factory
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

# Clase base
class Base(DeclarativeBase):
    pass


async def get_session():
    async with SessionLocal() as session:
        yield session

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync()  # Crea tables

def probar_conexion():
    try:
        with engine.connect() as connection:
            print("✅ Conectado a la base de datos exitosamente!")
    except Exception as e:
        print(f"❌ Error conectando la base de datos: {e}")
    finally:
        engine.dispose()

if __name__ == "__main__":
    probar_conexion()

