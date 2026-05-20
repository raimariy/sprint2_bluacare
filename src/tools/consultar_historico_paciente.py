"""
consultar_historico_paciente.py
Tool simulada: consultar_historico_paciente

Retorna histórico clínico realista de 3 pacientes sintéticos.
"""

# Base de dados simulada — 3 personas sintéticas
PACIENTES: dict = {
    "CP-00123": {
        "status": "sucesso",
        "paciente_id": "CP-00123",
        "nome": "Maria Silva",
        "idade": 34,
        "sexo": "feminino",
        "comorbidades": ["hipertensão arterial leve"],
        "medicamentos_uso_continuo": ["Losartana 50mg (1x/dia)"],
        "ultima_consulta": {
            "data": "2026-03-15",
            "especialidade": "clinica_geral",
            "medico": "Dr. João Mendes",
            "resumo": "Controle de PA — pressão estabilizada em 130/85"
        },
        "exames_recentes": [
            {"nome": "Hemograma completo", "data": "2026-02-10", "resultado": "Normal"},
            {"nome": "Creatinina",         "data": "2026-02-10", "resultado": "0.9 mg/dL (normal)"}
        ],
        "alergias": [],
        "plano": "Care Plus Executivo"
    },
    "CP-00456": {
        "status": "sucesso",
        "paciente_id": "CP-00456",
        "nome": "João Costa",
        "idade": 67,
        "sexo": "masculino",
        "comorbidades": ["diabetes tipo 2", "hipertensão arterial moderada"],
        "medicamentos_uso_continuo": [
            "Metformina 850mg (2x/dia)",
            "Enalapril 10mg (1x/dia)",
            "AAS 100mg (1x/dia)"
        ],
        "ultima_consulta": {
            "data": "2026-04-02",
            "especialidade": "endocrinologia",
            "medico": "Dra. Ana Lima",
            "resumo": "HbA1c 7.2% — controle glicêmico adequado"
        },
        "exames_recentes": [
            {"nome": "Glicemia em jejum", "data": "2026-04-01", "resultado": "128 mg/dL"},
            {"nome": "HbA1c",             "data": "2026-04-01", "resultado": "7.2%"}
        ],
        "alergias": ["Penicilina"],
        "plano": "Care Plus Premium"
    },
    "CP-00789": {
        "status": "sucesso",
        "paciente_id": "CP-00789",
        "nome": "Ana Souza",
        "idade": 28,
        "sexo": "feminino",
        "comorbidades": [],
        "medicamentos_uso_continuo": ["Anticoncepcional oral (Yasmin)"],
        "ultima_consulta": {
            "data": "2025-11-20",
            "especialidade": "ginecologia",
            "medico": "Dra. Carla Rocha",
            "resumo": "Check-up anual — sem alterações"
        },
        "exames_recentes": [
            {"nome": "Papanicolau", "data": "2025-11-20", "resultado": "Normal"}
        ],
        "alergias": [],
        "plano": "Care Plus Standard"
    }
}


def consultar_historico_paciente(paciente_id: str, janela_meses: int = 12) -> dict:
    """
    Retorna histórico clínico simulado do beneficiário Care Plus.

    Args:
        paciente_id: ID do beneficiário (ex: 'CP-00123')
        janela_meses: Janela retroativa em meses (default 12)

    Returns:
        Dicionário com dados clínicos do paciente ou mensagem de erro
    """
    if paciente_id not in PACIENTES:
        return {
            "status": "erro",
            "mensagem": f"Beneficiário {paciente_id} não encontrado na base Care Plus.",
            "paciente_id": paciente_id
        }

    resultado = PACIENTES[paciente_id].copy()
    resultado["janela_meses"] = janela_meses
    return resultado
