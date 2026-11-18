from fastapi import HTTPException, status

from app.domain.models import Cita, CitaCreate
from app.repositories.cita_repo import CitaRepository
from app.repositories.paciente_repo import PacienteRepository


class CitaService:

    def __init__(self, cita_repo: CitaRepository, paciente_repo: PacienteRepository):
        self.cita_repo = cita_repo
        self.paciente_repo = paciente_repo

    def crear_cita(self, data: CitaCreate) -> Cita:
        # Regla 1: el paciente debe existir
        paciente = self.paciente_repo.get_by_id(data.idPaciente)
        if not paciente:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="El paciente no existe en la base de datos")

        # Regla 2: el paciente debe estar activo
        if paciente.estado != "activo":
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                                detail="El paciente no está activo")

        # Regla 3: el fisioterapeuta no puede tener otra cita a esa hora
        if self.cita_repo.get_by_fisioterapeuta_y_hora(data.idFisioterapeuta, data.fechaHora):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail="El horario seleccionado no está disponible")

        return self.cita_repo.create(data)