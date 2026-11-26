from typing import Optional
from fastapi import APIRouter, Query, status

from app.core.dependencias import cita_service

router = APIRouter(prefix="/api/v1/citas", tags=["Citas"])


# HU-010: Consultar citas agendadas
@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    responses={
        200: {"description": "Consulta exitosa", "content": {"application/json": {"example": {
            "mensaje": "Consulta de citas exitosa",
            "data": [{"idCita": 501, "idPaciente": 101, "nombrePaciente": "Ana María Gómez",
                      "idFisioterapeuta": 12, "fechaHora": "2026-11-20T10:00:00",
                      "estado": "agendada"}],
            "success": True}}}},
        400: {"description": "Filtro inválido", "content": {"application/json": {"example": {
            "mensaje": "Fecha no válida. Use el formato YYYY-MM-DD", "data": None, "success": False}}}},
    },
)
def consultar_citas(
    idPaciente: Optional[int] = Query(None),
    idFisioterapeuta: Optional[int] = Query(None),
    estado: Optional[str] = Query(None),
    fecha_desde: Optional[str] = Query(None, description="YYYY-MM-DD"),
    fecha_hasta: Optional[str] = Query(None, description="YYYY-MM-DD"),
    documento: Optional[str] = Query(None, description="Cédula del paciente"),
):
    data = cita_service.consultar_citas(idPaciente, idFisioterapeuta, estado,
                                        fecha_desde, fecha_hasta, documento)
    return {
        "mensaje": "Consulta de citas exitosa" if data else "No se encontraron citas",
        "data": data,
        "success": True
    }