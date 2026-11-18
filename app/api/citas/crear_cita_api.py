from fastapi import APIRouter, status

from app.domain.models import CitaCreate
from app.core.dependencias import cita_service

router = APIRouter(prefix="/api/v1/citas", tags=["Citas"])


# HU-009: Crear cita
@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    responses={
        201: {"description": "Cita creada", "content": {"application/json": {"example": {
            "mensaje": "Cita creada exitosamente",
            "data": {"idCita": 501, "estado": "pendiente"}, "success": True}}}},
        400: {"description": "Datos incompletos", "content": {"application/json": {"example": {
            "mensaje": "Datos incompletos o con formato inválido", "data": None, "success": False}}}},
        404: {"description": "Paciente no existe", "content": {"application/json": {"example": {
            "mensaje": "Paciente no encontrado", "data": None, "success": False}}}},
        409: {"description": "Horario ocupado", "content": {"application/json": {"example": {
            "mensaje": "El horario seleccionado no está disponible", "data": None, "success": False}}}},
        422: {"description": "Paciente inactivo", "content": {"application/json": {"example": {
            "mensaje": "El paciente no está activo", "data": None, "success": False}}}},
    },
)
def crear_cita(data: CitaCreate):
    cita = cita_service.crear_cita(data)
    return {
        "mensaje": "Cita creada exitosamente",
        "data": {"idCita": cita.idCita, "estado": cita.estado},
        "success": True
    }