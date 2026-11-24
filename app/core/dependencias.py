from app.repositories.paciente_repo import PacienteRepository
from app.services.paciente_service import PacienteService
from app.repositories.cita_repo import CitaRepository
from app.services.cita_service import CitaService

# Una sola instancia para que todos los endpoints compartan los datos
repo = PacienteRepository()
paciente_service = PacienteService(repo)

cita_repo = CitaRepository()
cita_service = CitaService(cita_repo, repo)


from app.repositories.horario_repo import HorarioRepository
from app.services.horario_service import HorarioService

horario_repo = HorarioRepository()
horario_service = HorarioService(horario_repo)


from app.repositories.rutina_repo import RutinaRepository
from app.services.rutina_service import RutinaService

rutina_repo = RutinaRepository()
rutina_service = RutinaService(rutina_repo)