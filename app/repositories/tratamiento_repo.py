from typing import Optional
from app.domain.models import Tratamiento


class TratamientoRepository:
    """Tratamientos de prueba en memoria (hasta que exista la historia de registro de tratamientos)."""

    def __init__(self):
        self._db: dict[int, Tratamiento] = {
            15: Tratamiento(idTratamiento=15, idPaciente=101,
                            diagnostico="Esguince de rodilla grado II",
                            contraindicaciones=["EQUILIBRIO"]),
            16: Tratamiento(idTratamiento=16, idPaciente=102,
                            diagnostico="Tendinitis de hombro",
                            contraindicaciones=["FORTALECIMIENTO"]),
        }

    def get_by_id(self, id_tratamiento: int) -> Optional[Tratamiento]:
        return self._db.get(id_tratamiento)

    def get_by_paciente(self, id_paciente: int) -> Optional[Tratamiento]:
        # Busca el tratamiento de un paciente (lo usa el servicio de diagnóstico, HU-036)
        for t in self._db.values():
            if t.idPaciente == id_paciente:
                return t
        return None