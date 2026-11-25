from typing import Optional
from app.domain.models import Rutina, RutinaCreate


class RutinaRepository:
    """Simulamos el catálogo de rutinas con un diccionario."""

    def __init__(self):
        self._db: dict[int, Rutina] = {}
        self._next_id: int = 31

    def get_by_nombre(self, nombre: str) -> Optional[Rutina]:
        # Busca una rutina con el mismo nombre (sin importar mayúsculas)
        for rutina in self._db.values():
            if rutina.nombre.strip().lower() == nombre.strip().lower():
                return rutina
        return None

    def create(self, data: RutinaCreate) -> Rutina:
        rutina = Rutina(idRutina=self._next_id, **data.model_dump())
        self._db[self._next_id] = rutina
        self._next_id += 1
        return rutina
    
    def get_by_id(self, id_rutina: int) -> Optional[Rutina]:
        return self._db.get(id_rutina)