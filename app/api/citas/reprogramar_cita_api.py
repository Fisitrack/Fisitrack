from fastapi import APIRouter, status

from app.domain.models import CitaReprogramar
from app.core.dependencias import cita_service

router = APIRouter(prefix="/api/v1/citas", tags=["Citas"])


# HU-011: Reprogramar cita
@router.put(
    "/{id_cita}",
    status_code=status.HTTP_200_OK,
    responses={
        200: {"description": "Cita reprogramada", "content": {"application/json": {"example": {
            "mensaje": "Cita reprogramada exitosamente",
            "data": {"idCita": 501, "fechaHora": "2026-11-12T10:00:00", "estado": "agendada"},
            "success": True}}}},
        400: {"description": "Fecha inválida", "content": {"application/json": {"example": {
            "mensaje": "Fecha y hora no válidas. Use formato AAAA-MM-DDTHH:MM:SS y una fecha futura",
            "data": None, "success": False}}}},
        404: {"description": "Cita no encontrada", "content": {"application/json": {"example": {
            "mensaje": "Cita no encontrada", "data": None, "success": False}}}},
        409: {"description": "Horario ocupado", "content": {"application/json": {"example": {
            "mensaje": "El nuevo horario no está disponible", "data": None, "success": False}}}},
        422: {"description": "Estado no permite reprogramar", "content": {"application/json": {"example": {
            "mensaje": "La cita no puede reprogramarse en su estado actual", "data": None, "success": False}}}},
    },
)
def reprogramar_cita(id_cita: int, data: CitaReprogramar):
    cita = cita_service.reprogramar_cita(id_cita, data)
    return {
        "mensaje": "Cita reprogramada exitosamente",
        "data": {"idCita": cita.idCita, "fechaHora": cita.fechaHora.isoformat(),
                 "estado": cita.estado},
        "success": True
    }