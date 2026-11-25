from fastapi import FastAPI, Request, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.api.pacientes.registrar_paciente_api import router as registrar_paciente_router
from app.api.pacientes.consultar_paciente_api import router as consultar_paciente_router
from app.api.citas.crear_cita_api import router as crear_cita_router
from app.api.citas.consultar_citas_api import router as consultar_cita_router
from app.api.citas.reprogramar_cita_api import router as reprogramar_cita_router
from app.api.citas.cancelar_cita_api import router as cancelar_cita_router
from app.api.horarios.registrar_horario_api import router as registrar_horario_router
from app.api.rutinas.registrar_rutina_api import router as registrar_rutina_router
from app.api.tratamientos.asignar_rutina_api import router as asignar_rutina_router



app = FastAPI(
    title="Fisitrack",
    description="API REST de FisiTrack con arquitectura de capas",
    version="1.0.0"
)

# Registra los endpoints de pacientes
app.include_router(registrar_paciente_router)
app.include_router(consultar_paciente_router)
app.include_router(crear_cita_router)
app.include_router(consultar_cita_router)
app.include_router(reprogramar_cita_router)
app.include_router(cancelar_cita_router)
app.include_router(registrar_horario_router)
app.include_router(registrar_rutina_router)
app.include_router(asignar_rutina_router)


@app.get("/health")
def health():
    return {"status": "ok", "version": "1.0.0",
            "environment": "development"}


# Datos incompletos o con formato inválido -> 400 (como pide la HU-001)
@app.exception_handler(RequestValidationError)
def error_validacion(request: Request, exc: RequestValidationError):
    ruta = request.url.path
    if ruta.startswith("/api/v1/citas"):
        mensaje = "Fecha y hora no válidas. Use formato AAAA-MM-DDTHH:MM:SS y una fecha futura"
    elif ruta.startswith("/api/v1/horarios"):
        mensaje = "Formato inválido. Use fecha AAAA-MM-DD y hora HH:MM"
    elif ruta.startswith("/api/v1/rutinas"):
        faltantes = [str(e["loc"][-1]) for e in exc.errors() if e["type"] == "missing"]
        if faltantes:
            mensaje = "Faltan campos obligatorios: " + ", ".join(faltantes)
        elif any("duracion_minutos" in e["loc"] for e in exc.errors()):
            mensaje = "La duración debe ser un número entero mayor a cero"
        else:
            mensaje = "Datos inválidos o incompletos"
    else:
        mensaje = "Datos incompletos o con formato inválido"
    return JSONResponse(
        status_code=400,
        content={"mensaje": mensaje, "data": None, "success": False}
    )
# Otros errores (ej. documento duplicado 409) con el mismo formato
@app.exception_handler(HTTPException)
def error_http(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"mensaje": exc.detail, "data": None, "success": False}
    )
