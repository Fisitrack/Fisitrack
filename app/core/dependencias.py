from app.repositories.paciente_repo import PacienteRepository
from app.services.paciente_service import PacienteService
from app.repositories.cita_repo import CitaRepository
from app.services.cita_service import CitaService

# Una sola instancia para que todos los endpoints compartan los datos
repo = PacienteRepository()
paciente_service = PacienteService(repo)

cita_repo = CitaRepository()
cita_service = CitaService(cita_repo, repo)