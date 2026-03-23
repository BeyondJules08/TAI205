#1. Importaciones
from fastapi import FastAPI, status, HTTPException, Depends
from typing import Annotated
import asyncio
from pydantic import BaseModel, Field
import secrets
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import jwt
from jwt.exceptions import InvalidTokenError
from pwdlib import PasswordHash
from datetime import datetime, timedelta, timezone

# a. Configuraciones OAuth2
SECRET_KEY = "b29fb2689f12fc2ce6cb71418df9827766cd1a10a251b820b603a24d1f430373"
ALGORITHM = "HS256"

# b. Generación de Tokens (incluir limite max 30 minutos)
ACCESS_TOKEN_EXPIRE_MINUTES = 30

password_hash = PasswordHash.recommended()
# Contraseña encriptada por defecto para validación
DUMMY_HASH = password_hash.hash("585426")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None

class User(BaseModel):
    username: str

def authenticate_user(username: str, password: str):
    # En este ejemplo validamos con el usuario "Julian" y contraseña "585426"
    userAuth = secrets.compare_digest(username, "Julian")
    passAuth = secrets.compare_digest(password, "585426")
    if not (userAuth and passAuth):
        return False
    return User(username=username)

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# c. Implementar validación de tokens    # como se hacía originalmente con HTTPBasic
async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except InvalidTokenError:
        raise credentials_exception
    
    # Validamos que sea el usuario "Julian"
    if token_data.username != "Julian":
        raise credentials_exception
    return User(username=token_data.username)

#2. Inicializacion de la APP
app = FastAPI(
    title="miAPI_JWT",
    description="Julian Santiago",
    version="1.0.0",
)

# BD Ficticia
usuarios=[
    {"id":1, "nombre":"Julian", "apellidos":"Villalon", "edad":"20"},
    {"id":2, "nombre":"Eliseo", "apellidos":"Novas", "edad":"20"},
    {"id":3, "nombre":"Sacatripas", "apellidos":"Ripper", "edad":"30"},
]

# Creamos el modelo
class crear_usuario(BaseModel):
    id: int = Field(..., gt=0, description="ID del usuario")
    nombre: str = Field(..., min_length=3, max_length=50, example="Julian")
    edad: int = Field(..., ge=1, le=123, description="Edad del usuario")
    apellidos: str | None = None

# Autenticación para obtener token
@app.post("/token", tags=["Autenticación"])
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")

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
async def agrega_usuario(usuario: crear_usuario): #modelo
    for usr in usuarios:
        if usr["id"] == usuario.id: #validacion de id unico
            raise HTTPException(
                status_code=400,
                detail=" El id ya existe"
            )
    
    nuevo_usuario = {
        "id": usuario.id,
        "nombre": usuario.nombre,
        "apellidos": usuario.apellidos,
        "edad": usuario.edad
    }
    
    usuarios.append(nuevo_usuario)
    return {
        "mensaje": "usuario agregado correctamente",
        "status" : "200",
        "usuario": nuevo_usuario
    }
    
#PUT
# d. Protección de endpoints (PUT y DELETE)
@app.put("/v1/usuario/{id}", tags=["CRUD HTTP"])
async def actualiza_usuario(id: int, usuario: dict, current_user: User = Depends(get_current_user)):
    for usr in usuarios:
        if usr["id"] == id:
            usr["id"] = usuario.get("id", usr["id"])
            usr["nombre"] = usuario.get("nombre", usr["nombre"])
            usr["apellidos"] = usuario.get("apellidos", usr["apellidos"])
            usr["edad"] = usuario.get("edad", usr["edad"])
            return {
                "mensaje": f"usuario actualizado correctamente por {current_user.username}",
                "status" : "200",
                "usuario": usr
            }
    raise HTTPException(status_code=404, detail="Usuario no encontrado")

#DELETE
# d. Protección de endpoints (PUT y DELETE)
@app.delete("/v1/usuario/{id}", tags=["CRUD HTTP"])
async def elimina_usuario(id: int, current_user: User = Depends(get_current_user)):
    for usr in usuarios:
        if usr["id"] == id:
            usuario_eliminado = usr.copy()
            usuarios.remove(usr)
            return {
                "mensaje": f"usuario eliminado por {current_user.username}",
                "status" : "200",
                "usuario": usuario_eliminado
            }
    raise HTTPException(status_code=404, detail="Usuario no encontrado")