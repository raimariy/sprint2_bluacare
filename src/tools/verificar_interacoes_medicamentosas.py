"""
verificar_interacoes_medicamentosas.py
Tool simulada: verificar_interacoes_medicamentosas

Verifica interações entre medicamentos usando base de dados simulada.
Retorna severidade real (nenhuma/leve/moderada/grave) e recomendações.
"""

# Base simulada de interações conhecidas
# Chave: frozenset de 2 nomes (lowercase, apenas palavra principal)
INTERACOES: dict = {
    frozenset(["losartana", "ibuprofeno"]): {
        "severidade": "moderada",
        "descricao": (
            "Anti-inflamatórios como ibuprofeno podem reduzir o efeito "
            "anti-hipertensivo da Losartana e aumentar o risco de lesão renal."
        ),
        "recomendacao": (
            "Prefira Paracetamol como analgésico. Se ibuprofeno for necessário, "
            "uso breve com monitoramento da pressão arterial. Consulte o médico."
        )
    },
    frozenset(["metformina", "dexametasona"]): {
        "severidade": "grave",
        "descricao": (
            "Corticosteroides como Dexametasona aumentam a glicemia, "
            "podendo descompensar o diabetes tipo 2."
        ),
        "recomendacao": (
            "Uso somente com supervisão médica e monitoramento intensivo "
            "de glicemia. Não usar sem prescrição."
        )
    },
    frozenset(["aas", "ibuprofeno"]): {
        "severidade": "moderada",
        "descricao": (
            "Ibuprofeno pode antagonizar o efeito antiagregante do AAS "
            "e aumentar o risco de sangramento gastrointestinal."
        ),
        "recomendacao": (
            "Evitar a combinação. Consulte o médico para uma alternativa "
            "analgésica segura para quem usa AAS."
        )
    },
    frozenset(["anticoagulante", "ibuprofeno"]): {
        "severidade": "grave",
        "descricao": (
            "Anti-inflamatórios potencializam o efeito anticoagulante, "
            "aumentando significativamente o risco de sangramento."
        ),
        "recomendacao": (
            "Contraindicado sem supervisão médica. Paracetamol em doses "
            "habituais é a alternativa mais segura para quem usa anticoagulante."
        )
    },
    frozenset(["enalapril", "potassio"]): {
        "severidade": "moderada",
        "descricao": (
            "Inibidores da ECA como Enalapril podem elevar os níveis de "
            "potássio. Suplementação adicional pode causar hipercalemia."
        ),
        "recomendacao": (
            "Monitorar potássio sérico antes de iniciar suplementação. "
            "Consulte o médico."
        )
    }
}


def _normalizar(nome: str) -> str:
    """Extrai e normaliza o nome principal do medicamento para busca."""
    return nome.lower().split()[0].strip()


def verificar_interacoes_medicamentosas(
    medicamentos_em_uso: list[str],
    novo_medicamento: str
) -> dict:
    """
    Verifica interações entre medicamentos em uso e um novo medicamento.

    Args:
        medicamentos_em_uso: Lista de medicamentos que o paciente já usa
        novo_medicamento: Medicamento a verificar

    Returns:
        Dicionário com severidade e recomendações, ou confirmação de ausência de interação
    """
    novo_norm = _normalizar(novo_medicamento)

    for medicamento in medicamentos_em_uso:
        med_norm = _normalizar(medicamento)
        chave = frozenset([med_norm, novo_norm])

        if chave in INTERACOES:
            interacao = INTERACOES[chave]
            return {
                "status": "interacao_encontrada",
                "severidade": interacao["severidade"],
                "medicamentos_em_uso": medicamentos_em_uso,
                "novo_medicamento": novo_medicamento,
                "descricao": interacao["descricao"],
                "recomendacao": interacao["recomendacao"]
            }

    return {
        "status": "sem_interacao",
        "severidade": "nenhuma",
        "medicamentos_em_uso": medicamentos_em_uso,
        "novo_medicamento": novo_medicamento,
        "descricao": "Não foi encontrada interação clinicamente relevante entre os medicamentos informados.",
        "recomendacao": "Pode ser utilizado conforme orientação médica ou farmacêutica."
    }
