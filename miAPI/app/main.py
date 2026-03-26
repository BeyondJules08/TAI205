#1. Importaciones
from fastapi import FastAPI
from app.routers.varios import routerV
from app.routers.usuarios import routerU
from app.data.db import Base, engine
from app.data import usuario

#Crear tablas en la base de datos
usuario.Base.metadata.create_all(bind=engine)

#2. Inicializacion de la APP
app = FastAPI(
    title="miAPI",
    description="Julian Santiago",
    version="1.0.0",
    )

#3. Incluir routers
app.include_router(routerV)
app.include_router(routerU)