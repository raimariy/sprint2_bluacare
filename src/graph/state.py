"""
state.py

Define o estado compartilhado entre todos os nós do grafo LangGraph.
O estado é passado e atualizado a cada nó executado.
"""

from typing import TypedDict, Literal


class BluaState(TypedDict):
    """
    Estado compartilhado do grafo BluaDiagnostics.

    Cada campo é atualizado pelos nós conforme a conversa avança.
    """

    # Conversa
    mensagem_atual: str
    historico: list

    # Paciente
    paciente_id: str | None

    # Triagem
    sintomas_coletados: list
    urgencia: Literal["rotina", "urgente", "emergencia"]

    # Controle de fluxo
    red_flag_detectada: bool
    escalada_ativada: bool
    triagem_encerrada: bool

    # RAG
    contexto_rag: str

    # Roteamento
    intencao: Literal["triagem", "prescricao", "escalada", "out_of_scope"]
    proxima_acao: Literal["triagem", "prescricao", "escalada", "fim"]

    # Resposta final
    resposta_final: str
    agente_usado: str