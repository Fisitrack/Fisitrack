from typing import Optional
from app.domain.models import Asignacion, AsignacionCreate


class AsignacionRepository:
    """Asignaciones de rutinas a tratamientos (en memoria)."""

    def __init__(self):
        self._db: dict[int, Asignacion] = {}
        self._next_id: int = 71

    def get_vigente(self, id_tratamiento: int, id_rutina: int) -> Optional[Asignacion]:
        # Busca si esa rutina ya está asignada y vigente en el tratamiento
        for a in self._db.values():
            if a.idTratamiento == id_tratamiento and a.idRutina == id_rutina and a.estado == "vigente":
                return a
        return None

    def create(self, id_tratamiento: int, data: AsignacionCreate) -> Asignacion:
        asignacion = Asignacion(idAsignacion=self._next_id, idTratamiento=id_tratamiento,
                                **data.model_dump())
        self._db[self._next_id] = asignacion
        self._next_id += 1
        return asignacion