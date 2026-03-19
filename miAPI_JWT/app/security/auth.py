from fastapi import status,HTTPException, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials  # HTTPBasic para autenticacion basica, HTTPBasicCredentials para credenciales
import secrets # Para comparar credenciales

# Seguridad HTTP Basic
seguridad = HTTPBasic()
def verificar_peticion(credenciales: HTTPBasicCredentials = Depends(seguridad)):
    userAuth = secrets.compare_digest(credenciales.username, "julian")
    passAuth = secrets.compare_digest(credenciales.password, "585426")
    if not (userAuth and passAuth):
        raise HTTPException(
            status_code= status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales invalidas",
        )
    return credenciales.username
