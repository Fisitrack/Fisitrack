from fastapi import APIRouter, status

from app.domain.models import CitaCancelar
from app.core.dependencias import cita_service

router = APIRouter(prefix="/api/v1/citas", tags=["Citas"])


# HU-012: Cancelar cita con motivo
@router.delete(
    "/{id_cita}",
    status_code=status.HTTP_200_OK,
    responses={
        200: {"description": "Cita cancelada", "content": {"application/json": {"example": {
            "mensaje": "Cita cancelada exitosamente",
            "data": {"idCita": 501, "estado": "cancelada", "motivo": "El paciente no puede asistir"},
            "success": True}}}},
        400: {"description": "Motivo no enviado", "content": {"application/json": {"example": {
            "mensaje": "El motivo de cancelación es obligatorio", "data": None, "success": False}}}},
        404: {"description": "Cita no encontrada", "content": {"application/json": {"example": {
            "mensaje": "Cita no encontrada", "data": None, "success": False}}}},
        422: {"description": "Estado no permite cancelar", "content": {"application/json": {"example": {
            "mensaje": "La cita no puede cancelarse en su estado actual", "data": None, "success": False}}}},
    },
)
def cancelar_cita(id_cita: int, data: CitaCancelar):
    cita = cita_service.cancelar_cita(id_cita, data)
    return {
        "mensaje": "Cita cancelada exitosamente",
        "data": {"idCita": cita.idCita, "estado": cita.estado, "motivo": cita.motivo},
        "success": True
    }