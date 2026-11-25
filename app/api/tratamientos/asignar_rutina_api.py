from fastapi import APIRouter, status

from app.domain.models import AsignacionCreate
from app.core.dependencias import asignacion_service

router = APIRouter(prefix="/api/v1/tratamientos", tags=["Tratamientos"])


# HU-020: Asignar rutina personalizada a un tratamiento
@router.post(
    "/{id_tratamiento}/rutinas",
    status_code=status.HTTP_201_CREATED,
    responses={
        201: {"description": "Rutina asignada", "content": {"application/json": {"example": {
            "mensaje": "Rutina asignada exitosamente",
            "data": {"idAsignacion": 71, "idTratamiento": 15, "idRutina": 31,
                     "intensidad": "MEDIA", "estado": "vigente"},
            "success": True}}}},
        400: {"description": "Intensidad no válida", "content": {"application/json": {"example": {
            "mensaje": "Intensidad no válida. Utilice BAJA, MEDIA o ALTA", "data": None, "success": False}}}},
        404: {"description": "Tratamiento o rutina no encontrado", "content": {"application/json": {"example": {
            "mensaje": "Tratamiento no encontrado", "data": None, "success": False}}}},
        409: {"description": "Rutina ya asignada", "content": {"application/json": {"example": {
            "mensaje": "La rutina ya está asignada a este tratamiento", "data": None, "success": False}}}},
        422: {"description": "No coherente con el diagnóstico", "content": {"application/json": {"example": {
            "mensaje": "La rutina no es coherente con el diagnóstico del paciente", "data": None, "success": False}}}},
    },
)
def asignar_rutina(id_tratamiento: int, data: AsignacionCreate):
    a = asignacion_service.asignar_rutina(id_tratamiento, data)
    return {
        "mensaje": "Rutina asignada exitosamente",
        "data": {"idAsignacion": a.idAsignacion, "idTratamiento": a.idTratamiento,
                 "idRutina": a.idRutina, "intensidad": a.intensidad, "estado": a.estado},
        "success": True
    }