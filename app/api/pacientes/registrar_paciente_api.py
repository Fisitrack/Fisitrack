from fastapi import APIRouter, status

from app.domain.models import PacienteCreate
from app.core.dependencias import paciente_service

router = APIRouter(prefix="/api/v1/pacientes", tags=["Pacientes"])


# HU-001: Registrar paciente
@router.post("/", status_code=status.HTTP_201_CREATED)
def registrar_paciente(data: PacienteCreate):
    paciente = paciente_service.registrar_paciente(data)
    return {
        "mensaje": "Paciente registrado exitosamente",
        "data": {
            "idPaciente": paciente.idPaciente,
            "estado": paciente.estado
        },
        "success": True
    }