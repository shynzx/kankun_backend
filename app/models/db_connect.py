from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

def conexion_bd():
    db_user = "postgres"
    db_password = ""
    db_host = "localhost"  
    db_port = "5432"        
    db_name = "KanKunDB"

    engine = create_engine(f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}")
    return engine

def probar_conexion():
    # Probamos la conexión para luego cerrarla
    engine = conexion_bd()
    try:
        with engine.connect() as connection:
            print("Successfully connected to the database!")
    except Exception as e:
        print(f"Error connecting to the database: {e}")
    finally:
        engine.dispose()

if __name__ == "__main__":
    probar_conexion()
