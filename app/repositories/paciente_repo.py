from typing import Optional, List
from app.domain.models import Paciente, PacienteCreate


class PacienteRepository:
    """Simulamos una base de datos con un diccionario."""

    def __init__(self):
        self._db: dict[int, Paciente] = {}
        self._next_id: int = 101

    def get_all(self) -> List[Paciente]:
        return list(self._db.values())

    def get_by_id(self, id_paciente: int) -> Optional[Paciente]:
        return self._db.get(id_paciente)

    def get_by_documento(self, documento: str) -> Optional[Paciente]:
        # Busca si ya existe un paciente con ese documento
        for paciente in self._db.values():
            if paciente.documento == documento:
                return paciente
        return None

    def create(self, data: PacienteCreate) -> Paciente:
        paciente = Paciente(
            idPaciente=self._next_id,
            estado="activo",
            **data.model_dump()
        )
        self._db[self._next_id] = paciente
        self._next_id += 1
        return paciente