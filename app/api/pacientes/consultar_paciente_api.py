from fastapi import APIRouter, status

from app.core.dependencias import paciente_service

router = APIRouter(prefix="/api/v1/pacientes", tags=["Pacientes"])


# HU-002: Consultar paciente
@router.get("/{id_paciente}", status_code=status.HTTP_200_OK)
def consultar_paciente(id_paciente: int):
    paciente = paciente_service.consultar_paciente(id_paciente)
    return {
        "mensaje": "Consulta exitosa",
        "data": paciente.model_dump(),
        "success": True
    }