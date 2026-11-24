from app.domain.models import BloqueHorario


class HorarioRepository:
    """Simulamos la base de datos de horarios con un diccionario."""

    def __init__(self):
        # Fisioterapeutas de prueba (se reemplazan cuando exista la HU-085)
        self._fisioterapeutas = {12: "Fisioterapeuta 12", 15: "Fisioterapeuta 15"}
        # Bloques de horario registrados por cada fisioterapeuta
        self._bloques: dict[int, list[BloqueHorario]] = {}

    def existe_fisioterapeuta(self, id_fisio: int) -> bool:
        return id_fisio in self._fisioterapeutas

    def get_bloques(self, id_fisio: int) -> list[BloqueHorario]:
        # Devuelve los bloques que ya tiene registrados el fisioterapeuta
        return self._bloques.get(id_fisio, [])

    def guardar(self, id_fisio: int, bloques: list[BloqueHorario]) -> list[BloqueHorario]:
        # Agrega los bloques nuevos a los que ya tenía
        self._bloques.setdefault(id_fisio, []).extend(bloques)
        return bloques