"""
builder.py

Monta e compila o grafo LangGraph do BluaDiagnostics.

Estrutura do grafo:
  START → supervisor → [rag → triagem | rag → prescricao | escalada | out_of_scope] → END
"""

from langgraph.graph import StateGraph, END

from src.graph.state import BluaState
from src.graph.nodes import (
    no_supervisor,
    no_rag,
    no_triagem,
    no_prescricao,
    no_escalada,
    no_out_of_scope,
)


def rotear_apos_supervisor(state: BluaState) -> str:
    """
    Função de roteamento condicional após o supervisor.
    Define qual nó será executado a seguir.
    """
    if state.get("red_flag_detectada"):
        return "escalada"

    intencao = state.get("intencao", "triagem")

    if intencao == "prescricao":
        return "rag"
    elif intencao == "out_of_scope":
        return "out_of_scope"
    else:
        return "rag"  # triagem sempre passa pelo RAG


def rotear_apos_rag(state: BluaState) -> str:
    """
    Função de roteamento após o RAG.
    Decide entre triagem e prescrição.
    """
    intencao = state.get("intencao", "triagem")

    if intencao == "prescricao":
        return "prescricao"
    return "triagem"


def rotear_apos_triagem(state: BluaState) -> str:
    """
    Após a triagem, verifica se houve red flag detectada pelo LLM.
    """
    if state.get("red_flag_detectada"):
        return "escalada"
    return END


def build_graph() -> StateGraph:
    """
    Constrói e compila o grafo LangGraph.

    Returns:
        Grafo compilado pronto para uso
    """
    workflow = StateGraph(BluaState)

    # Adiciona os nós
    workflow.add_node("supervisor", no_supervisor)
    workflow.add_node("rag", no_rag)
    workflow.add_node("triagem", no_triagem)
    workflow.add_node("prescricao", no_prescricao)
    workflow.add_node("escalada", no_escalada)
    workflow.add_node("out_of_scope", no_out_of_scope)

    # Define ponto de entrada
    workflow.set_entry_point("supervisor")

    # Arestas condicionais a partir do supervisor
    workflow.add_conditional_edges(
        "supervisor",
        rotear_apos_supervisor,
        {
            "rag": "rag",
            "escalada": "escalada",
            "out_of_scope": "out_of_scope",
        },
    )

    # Após o RAG, decide entre triagem e prescrição
    workflow.add_conditional_edges(
        "rag",
        rotear_apos_rag,
        {
            "triagem": "triagem",
            "prescricao": "prescricao",
        },
    )

    # Após triagem, verifica se precisa escalar
    workflow.add_conditional_edges(
        "triagem",
        rotear_apos_triagem,
        {
            "escalada": "escalada",
            END: END,
        },
    )

    # Prescrição e escalada terminam o fluxo
    workflow.add_edge("prescricao", END)
    workflow.add_edge("escalada", END)
    workflow.add_edge("out_of_scope", END)

    grafo = workflow.compile()
    print("✅ Grafo LangGraph compilado!")
    return grafo


# Estado inicial padrão
def estado_inicial(mensagem: str, paciente_id: str = None) -> BluaState:
    """
    Cria o estado inicial para uma nova execução do grafo.

    Args:
        mensagem: primeira mensagem do usuário
        paciente_id: ID do beneficiário (opcional)

    Returns:
        Estado inicial do grafo
    """
    return BluaState(
        mensagem_atual=mensagem,
        historico=[],
        paciente_id=paciente_id,
        sintomas_coletados=[],
        urgencia="rotina",
        red_flag_detectada=False,
        escalada_ativada=False,
        triagem_encerrada=False,
        contexto_rag="",
        intencao="triagem",
        proxima_acao="triagem",
        resposta_final="",
        agente_usado="",
    )