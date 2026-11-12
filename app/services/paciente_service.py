from fastapi import HTTPException, status

from app.domain.models import Paciente, PacienteCreate
from app.repositories.paciente_repo import PacienteRepository


class PacienteService:

    def __init__(self, repo: PacienteRepository):
        self.repo = repo

    def registrar_paciente(self, data: PacienteCreate) -> Paciente:
        # Regla de negocio: no puede haber dos pacientes con el mismo documento
        if self.repo.get_by_documento(data.documento):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Ya existe un paciente registrado con ese documento"
            )
        return self.repo.create(data)