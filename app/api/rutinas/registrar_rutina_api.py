from fastapi import APIRouter, status

from app.domain.models import RutinaCreate
from app.core.dependencias import rutina_service

router = APIRouter(prefix="/api/v1/rutinas", tags=["Rutinas"])


# HU-016: Registrar rutina en el catálogo
@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    responses={
        201: {"description": "Rutina registrada", "content": {"application/json": {"example": {
            "mensaje": "Rutina registrada exitosamente", "data": {"idRutina": 31}, "success": True}}}},
        400: {"description": "Datos inválidos o incompletos", "content": {"application/json": {"example": {
            "mensaje": "La rutina debe tener al menos un ejercicio", "data": None, "success": False}}}},
        409: {"description": "Rutina duplicada", "content": {"application/json": {"example": {
            "mensaje": "Ya existe una rutina con ese nombre", "data": None, "success": False}}}},
    },
)
def registrar_rutina(data: RutinaCreate):
    rutina = rutina_service.registrar_rutina(data)
    return {
        "mensaje": "Rutina registrada exitosamente",
        "data": {"idRutina": rutina.idRutina},
        "success": True
    }