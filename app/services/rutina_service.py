from fastapi import HTTPException, status

from app.domain.models import Rutina, RutinaCreate
from app.repositories.rutina_repo import RutinaRepository

TIPOS_PERMITIDOS = ["FORTALECIMIENTO", "MOVILIDAD", "ESTIRAMIENTO", "EQUILIBRIO"]


class RutinaService:

    def __init__(self, repo: RutinaRepository):
        self.repo = repo

    def registrar_rutina(self, data: RutinaCreate) -> Rutina:
        # Regla 1: el nombre no puede estar vacío
        if not data.nombre.strip():
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="Faltan campos obligatorios: nombre")

        # Regla 2: al menos un ejercicio
        if not data.ejercicios:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="La rutina debe tener al menos un ejercicio")

        # Regla 3: duración mayor a cero
        if data.duracion_minutos <= 0:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="La duración debe ser un número entero mayor a cero")

        # Regla 4: tipo permitido
        if data.tipo.upper() not in TIPOS_PERMITIDOS:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="Tipo no permitido. Use: " + ", ".join(TIPOS_PERMITIDOS))

        # Regla 5: no puede haber otra rutina con el mismo nombre
        if self.repo.get_by_nombre(data.nombre):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail="Ya existe una rutina con ese nombre")

        data.tipo = data.tipo.upper()
        return self.repo.create(data)