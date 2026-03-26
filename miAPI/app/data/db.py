from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

# Definir la URL conexion con el contenedor
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://admin:123456@postgres:5432/DB_miapi")

# Crear motor de base de datos
engine = create_engine(DATABASE_URL)

# Definimos el manejador de sessiones 
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Instanciamos la base declarativa del modelo
Base = declarative_base()

# Funcion para obtener la sesion
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



