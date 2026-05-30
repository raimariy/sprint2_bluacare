"""
scope_validator.py

Valida se a mensagem está dentro do escopo do BluaDiagnostics.
Rejeita perguntas completamente fora do domínio de saúde e Care Plus.
"""

import re
from dataclasses import dataclass


@dataclass
class ResultadoScope:
    """Resultado da validação de escopo."""
    dentro_do_escopo: bool
    motivo: str | None
    resposta_sugerida: str | None


# Tópicos claramente fora do escopo
TOPICOS_OUT_OF_SCOPE = [
    # Finanças
    r"(dólar|euro|real|bitcoin|criptomoeda|ação|bolsa|investimento|cotação)",
    # Entretenimento
    r"(futebol|jogo|filme|série|música|novela|celebridade)",
    # Culinária não relacionada a saúde
    r"receita de (bolo|pizza|macarrão|frango|carne|pão)",
    # Política
    r"(político|eleição|presidente|governador|partido|voto)",
    # Outros serviços
    r"(uber|ifood|amazon|netflix|spotify|instagram|tiktok)",
    # Trabalho não relacionado
    r"(currículo|emprego|salário|e-mail para (chefe|patrão|empresa))",
]

# Tópicos claramente dentro do escopo
TOPICOS_IN_SCOPE = [
    r"(dor|febre|tosse|enjoo|náusea|tontura|cansaço|fadiga)",
    r"(medicamento|remédio|prescrição|receita médica|bula)",
    r"(consulta|médico|teleconsulta|agendamento|care plus|blua)",
    r"(sintoma|doença|saúde|exame|resultado|laboratório)",
    r"(pressão|diabetes|hipertensão|glicemia|colesterol)",
    r"(spo2|frequência cardíaca|temperatura|saturação|wearable)",
    r"(sono|exercício|alimentação saudável|prevenção|vacina)",
]


def validar_escopo(mensagem: str) -> ResultadoScope:
    """
    Verifica se a mensagem está dentro do escopo do sistema.

    Args:
        mensagem: texto do usuário

    Returns:
        ResultadoScope com resultado da validação
    """
    mensagem_lower = mensagem.lower()

    # Verifica se é claramente dentro do escopo
    for padrao in TOPICOS_IN_SCOPE:
        if re.search(padrao, mensagem_lower):
            return ResultadoScope(
                dentro_do_escopo=True,
                motivo=None,
                resposta_sugerida=None,
            )

    # Verifica se é claramente fora do escopo
    for padrao in TOPICOS_OUT_OF_SCOPE:
        if re.search(padrao, mensagem_lower):
            return ResultadoScope(
                dentro_do_escopo=False,
                motivo="topico_fora_do_escopo",
                resposta_sugerida=(
                    "Olá! Sou o BluaAssistente da Care Plus, especializado em saúde. "
                    "Não consigo te ajudar com esse assunto, mas posso te auxiliar com "
                    "triagem de sintomas, informações de saúde ou agendamento de "
                    "teleconsultas. Como posso te ajudar?"
                ),
            )

    # Dúvida — deixa passar para o LLM decidir
    return ResultadoScope(
        dentro_do_escopo=True,
        motivo=None,
        resposta_sugerida=None,
    )