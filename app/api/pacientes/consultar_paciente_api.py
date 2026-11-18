from fastapi import APIRouter, status

from app.core.dependencias import paciente_service

router = APIRouter(prefix="/api/v1/pacientes", tags=["Pacientes"])


# HU-002: Consultar paciente
@router.get(
    "/{id_paciente}",
    status_code=status.HTTP_200_OK,
    responses={
        200: {"description": "Consulta exitosa", "content": {"application/json": {"example": {
            "mensaje": "Consulta exitosa",
            "data": {"idPaciente": 101, "nombre": "Ana María Gómez", "documento": "1098765432",
                     "telefono": "3001234567", "correo": "ana.gomez@gmail.com",
                     "fechaNacimiento": "1995-04-20", "estado": "activo"},
            "success": True}}}},
        400: {"description": "Id inválido", "content": {"application/json": {"example": {
            "mensaje": "Datos incompletos o con formato inválido", "data": None, "success": False}}}},
        404: {"description": "Paciente no encontrado", "content": {"application/json": {"example": {
            "mensaje": "Paciente no encontrado", "data": None, "success": False}}}},
    },
)
def consultar_paciente(id_paciente: int):
    paciente = paciente_service.consultar_paciente(id_paciente)
    return {
        "mensaje": "Consulta exitosa",
        "data": paciente.model_dump(),
        "success": True
    }