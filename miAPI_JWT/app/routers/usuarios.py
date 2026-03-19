#3. Endpoints
from fastapi import HTTPException, Depends, APIRouter
from app.models.usuarios import crear_usuario
from app.data.database import usuarios
from app.security.auth import verificar_peticion

routerU = APIRouter(
    prefix="/v1/usuario",
    tags=["CRUD HTTP"]
)

#GET
@routerU.get("/")
async def consulta_usuarios():
    return{
        "status":"200",
        "total": len(usuarios),
        "data": usuarios
    }
#POST
@routerU.post("/")
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
@routerU.put("/{id}")
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
@routerU.delete("/{id}")
async def elimina_usuario(id: int, userAuth:str = Depends(verificar_peticion)):
    for usr in usuarios:
        if usr["id"] == id:
            usuarios.remove(usr)
            return {
                "mensaje": f"usuario eliminado por {userAuth}",
                "status" : "200",
                "usuario": usuario
            }