from fastapi import FastAPI, Request, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.api.router import router


app = FastAPI(
    title="Fisitrack",
    description="API REST de FisiTrack con arquitectura de capas",
    version="1.0.0"
)

# Registra los endpoints de pacientes
app.include_router(router)


@app.get("/health")
def health():
    return {"status": "ok", "version": "1.0.0",
            "environment": "development"}


# Datos incompletos o con formato inválido -> 400 (como pide la HU-001)
@app.exception_handler(RequestValidationError)
def error_validacion(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=400,
        content={
            "mensaje": "Datos incompletos o con formato inválido",
            "data": None,
            "success": False
        }
    )


# Otros errores (ej. documento duplicado 409) con el mismo formato
@app.exception_handler(HTTPException)
def error_http(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"mensaje": exc.detail, "data": None, "success": False}
    )