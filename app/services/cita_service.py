from datetime import datetime
from fastapi import HTTPException, status

from app.domain.models import Cita, CitaCreate, CitaReprogramar, CitaCancelar
from app.repositories.cita_repo import CitaRepository
from app.repositories.paciente_repo import PacienteRepository


class CitaService:

    def __init__(self, cita_repo: CitaRepository, paciente_repo: PacienteRepository):
        self.cita_repo = cita_repo
        self.paciente_repo = paciente_repo

    def crear_cita(self, data: CitaCreate) -> Cita:
        # Regla 1: no se permiten fechas pasadas
        if data.fechaHora <= datetime.now():
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="Fecha y hora no válidas. Use formato AAAA-MM-DDTHH:MM:SS y una fecha futura")

        # Regla 2: el paciente debe existir
        paciente = self.paciente_repo.get_by_id(data.idPaciente)
        if not paciente:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Paciente no encontrado")

        # Regla 3: el paciente debe estar activo
        if paciente.estado != "activo":
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                                detail="El paciente no está activo")

        # Regla 4: el fisioterapeuta no puede tener otra cita a esa hora
        if self.cita_repo.get_by_fisioterapeuta_y_hora(data.idFisioterapeuta, data.fechaHora):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail="El horario seleccionado no está disponible")

        return self.cita_repo.create(data)
    
    def consultar_citas(self, id_paciente=None, id_fisio=None, estado=None,
                        fecha_desde=None, fecha_hasta=None, documento=None):
        # Si se busca por cédula, se convierte en el id del paciente
        if documento is not None:
            paciente = self.paciente_repo.get_by_documento(documento)
            if not paciente:
                return []
            id_paciente = paciente.idPaciente

        # Regla 1: el estado debe ser uno de los válidosñ
        estados_validos = ["agendada", "confirmada", "cancelada", "atendida"]
        if estado is not None and estado not in estados_validos:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="Estado no válido. Use: agendada, confirmada, cancelada o atendida")

        # Regla 2: las fechas deben tener formato YYYY-MM-DD
        try:
            desde = datetime.strptime(fecha_desde, "%Y-%m-%d").date() if fecha_desde else None
            hasta = datetime.strptime(fecha_hasta, "%Y-%m-%d").date() if fecha_hasta else None
        except ValueError:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="Fecha no válida. Use el formato YYYY-MM-DD")

        citas = self.cita_repo.filtrar(id_paciente, id_fisio, estado, desde, hasta)
        resultado = []
        for c in citas:
            paciente = self.paciente_repo.get_by_id(c.idPaciente)
            resultado.append({
                "idCita": c.idCita,
                "idPaciente": c.idPaciente,
                "nombrePaciente": paciente.nombre if paciente else None,
                "idFisioterapeuta": c.idFisioterapeuta,
                "fechaHora": c.fechaHora.isoformat(),
                "estado": c.estado,
            })
        return resultado

    
    def reprogramar_cita(self, id_cita: int, data: CitaReprogramar) -> Cita:
        # Regla 1: la nueva fecha debe ser futura
        if data.fechaHora <= datetime.now():
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="Fecha y hora no válidas. Use formato AAAA-MM-DDTHH:MM:SS y una fecha futura")

        # Regla 2: la cita debe existir
        cita = self.cita_repo.get_by_id(id_cita)
        if not cita:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Cita no encontrada")

        # Regla 3: solo se reprograma si está agendada o confirmada
        if cita.estado not in ["agendada", "confirmada"]:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                                detail="La cita no puede reprogramarse en su estado actual")

        # Regla 4: el nuevo horario del fisioterapeuta debe estar libre
        otra = self.cita_repo.get_by_fisioterapeuta_y_hora(cita.idFisioterapeuta, data.fechaHora)
        if otra and otra.idCita != id_cita:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail="El nuevo horario no está disponible")

        return self.cita_repo.actualizar_fecha(id_cita, data.fechaHora)

    
    def cancelar_cita(self, id_cita: int, data: CitaCancelar) -> Cita:
        # Regla 1: el motivo es obligatorio
        if not data.motivo or not data.motivo.strip():
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="El motivo de cancelación es obligatorio")

        # Regla 2: la cita debe existir
        cita = self.cita_repo.get_by_id(id_cita)
        if not cita:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Cita no encontrada")

        # Regla 3: solo se cancela si está agendada o confirmada
        if cita.estado not in ["agendada", "confirmada"]:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                                detail="La cita no puede cancelarse en su estado actual")

        return self.cita_repo.cancelar(id_cita, data.motivo.strip())