from fastapi import FastAPI,status,HTTPException, Depends # HTTPException para errores, Depends para dependencias
from typing import Optional
import asyncio
from pydantic import BaseModel, Field
from fastapi.security import HTTPBasic, HTTPBasicCredentials # HTTPBasic para autenticacion basica, HTTPBasicCredentials para credenciales
import secrets # Para comparar credenciales

app = FastAPI(
    title="API Sistema de Reservas Hospedaje",
    description="Julian Santiago",
    version="1.0.0",
    )

# BD Ficticia
reservas=[
    {"id":1, "huesped":"Julian", "fecha_actual:":15,"fecha_de_entrada:":17, "fecha_de_salida":20,"tipo_habitacion":"sencilla", "dias_estancia":1, "estado_reserva":"confirmado"},
    {"id":2, "huesped":"Eliseo", "fecha_actual:":15,"fecha_de_entrada":19, "fecha_de_salida":22,"tipo_habitacion":"doble", "dias_estancia":2, "estado_reserva":"pendiente"},
    {"id":3, "huesped":"Sacatripas", "fecha_actual:":15,"fecha_de_entrada":20, "fecha_de_salida":23,"tipo_habitacion":"suite", "dias_estancia":3, "estado_reserva":"cancelado"}
]

class crear_reserva(BaseModel):
    id:int = Field(..., gt=0, description="ID del huesped")
    huesped:str = Field(..., min_length=5, max_length=50, example="Julian")
    fecha_actual:int= Field(..., ge=1, le=2, example="15")
    fecha_de_entrada:int = Field(...,ge=1, le=2, description="Fecha de entrada no menor a fecha actual")
    fecha_de_salida:int= Field(..., ge=1, le=2, description="Fecha de salida mayor que fecha de entrada")
    tipo_habitacion:str = Field(..., min_length=5, max_length=8, example="sencilla",)
    dias_estancia:int = Field(..., ge=1, le=7, description="Dias de estancia")
    estado_reserva:str = Field(..., min_length=5, max_length=50, example="confirmado")
    
seguridad = HTTPBasic()
def verificar_peticion(credenciales: HTTPBasicCredentials = Depends(seguridad)):
    userAuth = secrets.compare_digest(credenciales.username, "hotel")
    passAuth = secrets.compare_digest(credenciales.password, "r2026")
    if not (userAuth and passAuth):
        raise HTTPException(
            status_code= status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales invalidas",
        )
    return credenciales.username

# Crear reservas POST
@app.post("/v1/reservas/", tags=["CRUD HTTP"])
async def crear_reserva(reserva:crear_reserva, userAuth:str = Depends(verificar_peticion)):
    for rev in reservas:
        if rev["id"] == reserva.id: #validacion de id unico
            raise HTTPException(
                status_code=400,
                detail=" El id ya existe"
            )
    reservas.append(reserva)
    return {
        "mensaje": "Reserva agregada correctamente",
        "status" : "200",
        "reserva":reserva
    }
    
# Listar reservas GET
@app.get("/v1/reservas/", tags=["CRUD HTTP"])
async def consulta_reservas():
    return{
        "status":"200",
        "total": len(reservas),
        "data": reservas
    }
    
# Consultar por ID GET
@app.get("/v1/reservas{id}", tags=["CRUD HTTP"])
async def consulta_uno(id: int):
    return {"Resultado":"Reserva encontrada",
            "estatus":"200"
            }
    
# Confirmar reserva PUT
@app.put("/v1/reservas/{id}", tags=["CRUD HTTP"])
async def actualiza_reserva(id: int, reserva:dict):
    for rev in reservas:
        if rev["id"] == id:
            rev["estado_reserva"] = reserva.get("estado_reserva")
            return {
                "mensaje": "Reserva confirmada correctamente",
                "status" : "200",
                "reserva": reserva
            }
            
# Cancelar reserva DELETE
@app.delete("/v1/reservas/{id}", tags=["CRUD HTTP"])
async def elimina_reserva(id: int, userAuth:str = Depends(verificar_peticion)):
    for rev in reservas:
        if rev["id"] == id:
            reservas.remove(rev)
            return {
                "mensaje": f" eliminado por {userAuth}",
                "status" : "200",
                "reserva": reserva
            }
