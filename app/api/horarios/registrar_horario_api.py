from fastapi import APIRouter, status

from app.domain.models import HorarioCreate
from app.core.dependencias import horario_service

router = APIRouter(prefix="/api/v1/horarios", tags=["Horarios"])


# HU-013: Registrar horario disponible
@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    responses={
        201: {"description": "Horario registrado", "content": {"application/json": {"example": {
            "mensaje": "Horario registrado exitosamente",
            "data": {"idFisioterapeuta": 12, "bloques": [
                {"fecha": "2026-12-01", "hora_inicio": "08:00", "hora_fin": "12:00"}]},
            "success": True}}}},
        400: {"description": "Datos inválidos", "content": {"application/json": {"example": {
            "mensaje": "La hora de fin debe ser posterior a la hora de inicio", "data": None, "success": False}}}},
        404: {"description": "Fisioterapeuta no encontrado", "content": {"application/json": {"example": {
            "mensaje": "Fisioterapeuta no encontrado", "data": None, "success": False}}}},
        409: {"description": "Bloques cruzados", "content": {"application/json": {"example": {
            "mensaje": "Los bloques de horario se cruzan con la disponibilidad existente",
            "data": None, "success": False}}}},
    },
)
def registrar_horario(data: HorarioCreate):
    bloques = horario_service.registrar_horario(data)
    return {
        "mensaje": "Horario registrado exitosamente",
        "data": {
            "idFisioterapeuta": data.idFisioterapeuta,
            "bloques": [{"fecha": b.fecha.isoformat(),
                         "hora_inicio": b.hora_inicio.strftime("%H:%M"),
                         "hora_fin": b.hora_fin.strftime("%H:%M")} for b in bloques],
        },
        "success": True
    }