from fastapi import HTTPException, status

from app.domain.models import Asignacion, AsignacionCreate
from app.repositories.asignacion_repo import AsignacionRepository
from app.repositories.rutina_repo import RutinaRepository
from app.repositories.tratamiento_repo import TratamientoRepository

INTENSIDADES = ["BAJA", "MEDIA", "ALTA"]


class AsignacionService:

    def __init__(self, asignacion_repo: AsignacionRepository,
                 rutina_repo: RutinaRepository, tratamiento_repo: TratamientoRepository):
        self.asignacion_repo = asignacion_repo
        self.rutina_repo = rutina_repo
        self.tratamiento_repo = tratamiento_repo

    def asignar_rutina(self, id_tratamiento: int, data: AsignacionCreate) -> Asignacion:
        # Regla 1: intensidad permitida
        if data.intensidad.upper() not in INTENSIDADES:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="Intensidad no válida. Utilice BAJA, MEDIA o ALTA")

        # Regla 2: el tratamiento debe existir
        tratamiento = self.tratamiento_repo.get_by_id(id_tratamiento)
        if not tratamiento:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Tratamiento no encontrado")

        # Regla 3: la rutina debe existir
        rutina = self.rutina_repo.get_by_id(data.idRutina)
        if not rutina:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Rutina no encontrada")

        # Regla 4: coherencia con el diagnóstico (HU-036)
        if rutina.tipo in tratamiento.contraindicaciones:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                                detail="La rutina no es coherente con el diagnóstico del paciente")

        # Regla 5: no repetir la misma rutina vigente
        if self.asignacion_repo.get_vigente(id_tratamiento, data.idRutina):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail="La rutina ya está asignada a este tratamiento")

        data.intensidad = data.intensidad.upper()
        return self.asignacion_repo.create(id_tratamiento, data)