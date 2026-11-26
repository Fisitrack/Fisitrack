from pydantic import BaseModel, Field
from datetime import date


# ── Modelo base: datos que envía el recepcionista ──
class PacienteBase(BaseModel):
    nombre: str = Field(..., min_length=3, max_length=100)
    documento: str = Field(..., pattern=r"^\d{6,10}$")
    telefono: str = Field(..., pattern=r"^\d{10}$")
    correo: str = Field(..., pattern=r"^[\w\.-]+@[\w\.-]+\.\w+$")
    fechaNacimiento: date


# ── Para CREAR un paciente (sin id) ──
class PacienteCreate(PacienteBase):
    pass


# ── Paciente completo (con id y estado) ──
class Paciente(PacienteBase):
    idPaciente: int
    estado: str = "activo"

    class Config:
        from_attributes = True



# ── HU-009: Citas ──
from datetime import datetime


class CitaCreate(BaseModel):
    idPaciente: int
    idFisioterapeuta: int
    fechaHora: datetime


class Cita(CitaCreate):
    idCita: int
    estado: str = "agendada"
    motivo: str | None = None


# ── HU-011: Reprogramar cita ──
class CitaReprogramar(BaseModel):
    fechaHora: datetime    



# ── HU-012: Cancelar cita ──
class CitaCancelar(BaseModel):
    motivo: str | None = None



# ── HU-013: Registrar horario disponible ──
from datetime import time


class BloqueHorario(BaseModel):
    fecha: date
    hora_inicio: time
    hora_fin: time


class HorarioCreate(BaseModel):
    idFisioterapeuta: int
    bloques: list[BloqueHorario]



# ── HU-016: Registrar rutina en el catálogo ──
class Ejercicio(BaseModel):
    nombre: str
    series: int
    repeticiones: int


class RutinaCreate(BaseModel):
    nombre: str
    ejercicios: list[Ejercicio]
    duracion_minutos: int
    tipo: str


class Rutina(RutinaCreate):
    idRutina: int



# ── HU-020: Asignar rutina a un tratamiento ──
class Tratamiento(BaseModel):
    idTratamiento: int
    idPaciente: int
    diagnostico: str
    contraindicaciones: list[str]


class AsignacionCreate(BaseModel):
    idRutina: int
    intensidad: str
    restricciones: str | None = None


class Asignacion(AsignacionCreate):
    idAsignacion: int
    idTratamiento: int
    estado: str = "vigente"        