from typing import Optional, List
from datetime import datetime
from app.domain.models import Cita, CitaCreate


class CitaRepository:
    """Simulamos una base de datos de citas con un diccionario."""

    def __init__(self):
        self._db: dict[int, Cita] = {}
        self._next_id: int = 501

    def get_all(self) -> List[Cita]:
        return list(self._db.values())

    def get_by_fisioterapeuta_y_hora(self, id_fisio: int, fecha_hora: datetime) -> Optional[Cita]:
        # Busca si el fisioterapeuta ya tiene una cita a esa hora
        for cita in self._db.values():
            if cita.idFisioterapeuta == id_fisio and cita.fechaHora == fecha_hora:
                return cita
        return None

    def create(self, data: CitaCreate) -> Cita:
        cita = Cita(idCita=self._next_id, estado="pendiente", **data.model_dump())
        self._db[self._next_id] = cita
        self._next_id += 1
        return cita