from datetime import date
from fastapi import HTTPException, status

from app.domain.models import BloqueHorario, HorarioCreate
from app.repositories.horario_repo import HorarioRepository


def se_cruzan(a: BloqueHorario, b: BloqueHorario) -> bool:
    # Dos bloques se cruzan si son el mismo día y sus horas se pisan
    return a.fecha == b.fecha and a.hora_inicio < b.hora_fin and b.hora_inicio < a.hora_fin


class HorarioService:

    def __init__(self, repo: HorarioRepository):
        self.repo = repo

    def registrar_horario(self, data: HorarioCreate) -> list[BloqueHorario]:
        # Regla 1: debe enviar al menos un bloque
        if not data.bloques:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="Debe enviar al menos un bloque de horario")

        # Regla 2: en cada bloque, fin después del inicio y fecha no pasada
        for b in data.bloques:
            if b.hora_fin <= b.hora_inicio:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                    detail="La hora de fin debe ser posterior a la hora de inicio")
            if b.fecha < date.today():
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                    detail="No se permiten bloques en fechas pasadas. Use fecha AAAA-MM-DD y hora HH:MM")

        # Regla 3: el fisioterapeuta debe existir
        if not self.repo.existe_fisioterapeuta(data.idFisioterapeuta):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Fisioterapeuta no encontrado")

        # Regla 4: los bloques enviados no se pueden cruzar entre sí
        for i, a in enumerate(data.bloques):
            for b in data.bloques[i + 1:]:
                if se_cruzan(a, b):
                    raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                        detail="Los bloques de horario se cruzan con la disponibilidad existente")

        # Regla 5: tampoco con los bloques que ya tiene registrados
        for a in data.bloques:
            for b in self.repo.get_bloques(data.idFisioterapeuta):
                if se_cruzan(a, b):
                    raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                        detail="Los bloques de horario se cruzan con la disponibilidad existente")

        return self.repo.guardar(data.idFisioterapeuta, data.bloques)