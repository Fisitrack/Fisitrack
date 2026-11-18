from app.repositories.paciente_repo import PacienteRepository
from app.services.paciente_service import PacienteService

# Una sola instancia para que todos los endpoints compartan los datos
repo = PacienteRepository()
paciente_service = PacienteService(repo)