#1. Importaciones
from fastapi import FastAPI,status,HTTPException
from typing import Optional
import asyncio
from pydantic import BaseModel, Field

#2. Inicializacion de la APP
app = FastAPI(
    title="miAPI",
    description="Julian Santiago",
    version="1.0.0",
    )
# BD Ficticia
usuarios=[
    {"id":"1", "nombre":"Julian", "apellidos":"Villalon", "edad":"20"},
    {"id":"2", "nombre":"Eliseo", "apellidos":"Novas", "edad":"20"},
    {"id":"3", "nombre":"Sacatripas", "apellidos":"Ripper", "edad":"30"},
]
#Creamos el modelo
class crear_usuario(BaseModel):
    id:int = Field(..., gt=0, description="ID del usuario")
    nombre:str = Field(..., min_length=3, max_length=50, example="Julian")
    edad:int = Field(..., ge=1, le=123, description="Edad del usuario")

#3. Endpoints
@app.get("/", tags=["Inicio"])
async def holaMundo():
    return {"mensaje":"Hola mundo FastAPI"}

@app.get("/v1/bienvenidos", tags=["Inicio"])
async def bien():
    return {"mensaje":"Bienvenidos"}

@app.get("/v1/promedio", tags=["Calificaciones"])
async def promedio():
    await asyncio.sleep(3) #simulacion peticion, consultaBD...
    return {
        "Calificacion":"9",
        "estatus":"200"
    }
@app.get("/v1/parametro0/{id}", tags=["Parametros"])
async def consulta_uno(id: str):
    return {"Resultado":"usuario no encontrado",
            "estatus":"200"
            }
#GET
@app.get("/v1/usuario/", tags=["CRUD HTTP"])
async def consulta_usuarios():
    return{
        "status":"200",
        "total": len(usuarios),
        "data": usuarios
    }
#POST
@app.post("/v1/usuario/", tags=["CRUD HTTP"])
async def crear_usuario(usuario:crear_usuario): #modelo
    for usr in usuarios:
        if usr["id"] == usuario.id: #validacion de id unico
            raise HTTPException(
                status_code=400,
                detail=" El id ya existe"
            )
    usuarios.append(usuario)
    return {
        "mensaje": "usuario agregado correctamente",
        "status" : "200",
        "usuario":usuario
    }
#PUT
@app.put("/v1/usuario/{id}", tags=["CRUD HTTP"])
async def actualiza_usuario(id: str, usuario:dict):
    for usr in usuarios:
        if usr["id"] == id:
            usr["id"] = usuario.get("id")
            usr["nombre"] = usuario.get("nombre")
            usr["apellidos"] = usuario.get("apellidos")
            usr["edad"] = usuario.get("edad")
            return {
                "mensaje": "usuario actualizado correctamente",
                "status" : "200",
                "usuario": usuario
            }
#DELETE
@app.delete("/v1/usuario/{id}", tags=["CRUD HTTP"])
async def elimina_usuario(id: str):
    for usr in usuarios:
        if usr["id"] == id:
            usuarios.remove(usr)
            return {
                "mensaje": "usuario eliminado correctamente",
                "status" : "200",
                "usuario": usuario
            }