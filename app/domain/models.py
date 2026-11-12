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