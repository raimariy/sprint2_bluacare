"""
agendar_teleconsulta.py
Tool simulada: agendar_teleconsulta

Agenda teleconsulta com retorno realista: código, link, data/hora calculada.
"""

from datetime import datetime, timedelta
import random


def agendar_teleconsulta(
    paciente_id: str,
    especialidade: str,
    urgencia: str,
    motivo: str = ""
) -> dict:
    """
    Agenda uma teleconsulta para o beneficiário Care Plus.

    Args:
        paciente_id: ID do beneficiário (ex: 'CP-00123')
        especialidade: Especialidade médica ('clinica_geral', 'cardiologia', etc.)
        urgencia: Nível de urgência ('rotina', 'urgente', 'emergencia')
        motivo: Breve descrição do motivo da consulta (opcional)

    Returns:
        Dicionário com confirmação do agendamento, link e instruções
    """
    especialidades_validas = {
        "clinica_geral", "cardiologia", "dermatologia",
        "pediatria", "ginecologia", "psiquiatria",
        "ortopedia", "oftalmologia"
    }
    urgencias_validas = {"rotina", "urgente", "emergencia"}

    # Validação de parâmetros
    if especialidade not in especialidades_validas:
        return {
            "status": "erro",
            "mensagem": f"Especialidade '{especialidade}' não disponível. "
                        f"Opções: {sorted(especialidades_validas)}"
        }

    if urgencia not in urgencias_validas:
        return {
            "status": "erro",
            "mensagem": f"Urgência '{urgencia}' inválida. Opções: rotina, urgente, emergencia"
        }

    # Calcula data/hora conforme urgência
    delta_por_urgencia = {
        "rotina":    timedelta(days=3),
        "urgente":   timedelta(hours=4),
        "emergencia": timedelta(minutes=30)
    }
    data_consulta = datetime.now() + delta_por_urgencia[urgencia]
    codigo = random.randint(10000, 99999)

    return {
        "status": "confirmado",
        "codigo_consulta": f"TC-{codigo}",
        "paciente_id": paciente_id,
        "especialidade": especialidade,
        "urgencia": urgencia,
        "motivo": motivo,
        "data_hora": data_consulta.strftime("%d/%m/%Y às %H:%M"),
        "medico": "Dr(a). a confirmar",
        "link_acesso": f"https://blua.careplus.com.br/teleconsulta/TC-{codigo}",
        "instrucoes": (
            "Acesse o link 5 minutos antes do horário. "
            "Tenha em mãos sua carteirinha Care Plus e documentos de identidade."
        )
    }
