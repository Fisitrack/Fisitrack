from datetime import datetime
from fastapi import HTTPException, status

from app.domain.models import Cita, CitaCreate
from app.repositories.cita_repo import CitaRepository
from app.repositories.paciente_repo import PacienteRepository


class CitaService:

    def __init__(self, cita_repo: CitaRepository, paciente_repo: PacienteRepository):
        self.cita_repo = cita_repo
        self.paciente_repo = paciente_repo

    def crear_cita(self, data: CitaCreate) -> Cita:
        # Regla 1: no se permiten fechas pasadas
        if data.fechaHora <= datetime.now():
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="Fecha y hora no válidas. Use formato AAAA-MM-DDTHH:MM:SS y una fecha futura")

        # Regla 2: el paciente debe existir
        paciente = self.paciente_repo.get_by_id(data.idPaciente)
        if not paciente:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Paciente no encontrado")

        # Regla 3: el paciente debe estar activo
        if paciente.estado != "activo":
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                                detail="El paciente no está activo")

        # Regla 4: el fisioterapeuta no puede tener otra cita a esa hora
        if self.cita_repo.get_by_fisioterapeuta_y_hora(data.idFisioterapeuta, data.fechaHora):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail="El horario seleccionado no está disponible")

        return self.cita_repo.create(data)