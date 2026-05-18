def agendar_teleconsulta(
    paciente_id: str,
    especialidade: str,
    urgencia: str
):
    return {
        "status": "agendado",
        "especialidade": especialidade,
        "urgencia": urgencia
    }