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
         if cita.idFisioterapeuta == id_fisio and cita.fechaHora == fecha_hora and cita.estado != "cancelada":
                 return cita
        return None

    def create(self, data: CitaCreate) -> Cita:
        cita = Cita(idCita=self._next_id, estado="agendada", **data.model_dump())
        self._db[self._next_id] = cita
        self._next_id += 1
        return cita

    def filtrar(self, id_paciente=None, id_fisio=None, estado=None,
                fecha_desde=None, fecha_hasta=None) -> List[Cita]:
        # Devuelve solo las citas que cumplen los filtros enviados
        citas = list(self._db.values())
        if id_paciente is not None:
            citas = [c for c in citas if c.idPaciente == id_paciente]
        if id_fisio is not None:
            citas = [c for c in citas if c.idFisioterapeuta == id_fisio]
        if estado is not None:
            citas = [c for c in citas if c.estado == estado]
        if fecha_desde is not None:
            citas = [c for c in citas if c.fechaHora.date() >= fecha_desde]
        if fecha_hasta is not None:
            citas = [c for c in citas if c.fechaHora.date() <= fecha_hasta]
        return citas

    
    def get_by_id(self, id_cita: int) -> Optional[Cita]:
        # Busca una cita por su id
        return self._db.get(id_cita)

    def actualizar_fecha(self, id_cita: int, nueva_fecha: datetime) -> Cita:
        # Cambia la fecha y hora de la cita (el horario anterior queda libre)
        cita = self._db[id_cita]
        cita.fechaHora = nueva_fecha
        return cita

    
    def cancelar(self, id_cita: int, motivo: str) -> Cita:
        # Cambia el estado a cancelada y guarda el motivo (no borra la cita)
        cita = self._db[id_cita]
        cita.estado = "cancelada"
        cita.motivo = motivo
        return cita