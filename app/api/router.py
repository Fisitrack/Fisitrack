from fastapi import APIRouter, status

from app.domain.models import PacienteCreate
from app.repositories.paciente_repo import PacienteRepository
from app.services.paciente_service import PacienteService


router = APIRouter(prefix="/api/v1/pacientes", tags=["Pacientes"])

# Se crea una sola vez para que los datos no se pierdan entre peticiones
repo = PacienteRepository()
service = PacienteService(repo)


# HU-001: Registrar paciente
@router.post("/", status_code=status.HTTP_201_CREATED)
def registrar_paciente(data: PacienteCreate):
    paciente = service.registrar_paciente(data)
    return {
        "mensaje": "Paciente registrado exitosamente",
        "data": {
            "idPaciente": paciente.idPaciente,
            "estado": paciente.estado
        },
        "success": True
    }