#1. Importaciones
from fastapi import FastAPI
from app.routers.varios import routerV
from app.routers.usuarios import routerU

#2. Inicializacion de la APP
app = FastAPI(
    title="miAPI JWT",
    description="Julian Santiago",
    version="1.0.0",
    )

#3. Incluir routers
app.include_router(routerV)
app.include_router(routerU)