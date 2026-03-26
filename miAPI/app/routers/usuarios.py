#3. Endpoints
from fastapi import HTTPException, Depends, APIRouter
from app.models.usuarios import crear_usuario
from app.data.database import usuarios
from app.security.auth import verificar_peticion

from sqlalchemy.orm import Session
from app.data.db import get_db
from app.data.usuario import usuario as usuarioDB

routerU = APIRouter(
    prefix="/v1/usuario",
    tags=["CRUD HTTP"]
)

#GET
@routerU.get("/")
async def consulta_usuarios(db: Session = Depends(get_db)):
    usuarios = db.query(usuarioDB).all()
    return{
        "status":"200",
        "total": len(usuarios),
        "data": usuarios
    }
    
#POST
@routerU.post("/")
async def crear_usuario(usuarioP:crear_usuario, db:Session = Depends(get_db)): #modelo
    
    usuarioNuevo = usuarioDB(
        nombre = usuarioP.nombre,
        edad = usuarioP.edad
    )
    db.add(usuarioNuevo)
    db.commit()
    db.refresh(usuarioNuevo)
    
    return {
        "mensaje": "usuario agregado correctamente",
        "status" : "200",
        "usuario":usuarioP
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