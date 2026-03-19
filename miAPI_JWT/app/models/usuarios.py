from pydantic import BaseModel, Field

#Creamos el modelo
class crear_usuario(BaseModel):
    id:int = Field(..., gt=0, description="ID del usuario")
    nombre:str = Field(..., min_length=3, max_length=50, example="Julian")
    edad:int = Field(..., ge=1, le=123, description="Edad del usuario")
