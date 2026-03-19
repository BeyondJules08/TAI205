from fastapi import APIRouter # HTTPException para errores, Depends para dependencias
from app.data.database import usuarios
from typing import Optional
import asyncio

routerV = APIRouter(
    tags=["Inicio"]
)

#3. Endpoints
@routerV.get("/")
async def holaMundo():
    return {"mensaje":"Hola mundo FastAPI"}

@routerV.get("/v1/bienvenidos")
async def bien():
    return {"mensaje":"Bienvenidos"}

@routerV.get("/v1/promedio")
async def promedio():
    await asyncio.sleep(3) #simulacion peticion, consultaBD...
    return {
        "Calificacion":"9",
        "estatus":"200"
    }
@routerV.get("/v1/parametro0/{id}")
async def consulta_uno(id: str):
    return {"Resultado":"usuario no encontrado",
            "estatus":"200"
            }
    