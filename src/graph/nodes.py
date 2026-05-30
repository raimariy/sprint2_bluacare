"""
nodes.py

Define os nós do grafo LangGraph.
Cada nó recebe o estado, executa uma ação e retorna o estado atualizado.
"""

import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from src.graph.state import BluaState
from src.agents.triagem import agente_triagem
from src.agents.prescricao import agente_prescricao
from src.agents.escalada import agente_escalada
from src.agents.supervisor import detectar_intencao, detectar_red_flag
from src.rag.retriever import buscar_contexto


def no_supervisor(state: BluaState) -> BluaState:
    """
    Nó supervisor — detecta intenção e roteia para o próximo nó.
    """
    print(f"\n[NÓ: supervisor] Mensagem: {state['mensagem_atual'][:50]}...")

    mensagem = state["mensagem_atual"]

    # Detecta red flag imediatamente
    if detectar_red_flag(mensagem):
        print("[NÓ: supervisor] Red flag detectada → escalada")
        return {
            **state,
            "red_flag_detectada": True,
            "intencao": "escalada",
            "proxima_acao": "escalada",
        }

    # Detecta intenção
    intencao = detectar_intencao(mensagem)
    proxima_acao = intencao if intencao != "out_of_scope" else "fim"

    print(f"[NÓ: supervisor] Intenção: {intencao}")

    return {
        **state,
        "intencao": intencao,
        "proxima_acao": proxima_acao,
    }


def no_rag(state: BluaState) -> BluaState:
    """
    Nó RAG — busca contexto relevante na base de conhecimento.
    Executado antes da triagem e prescrição.
    """
    print("[NÓ: rag] Buscando contexto...")

    try:
        from src.rag.vector_store import carregar_vector_store
        vs = carregar_vector_store()
        contexto = buscar_contexto(state["mensagem_atual"], vs, k=2)
        print(f"[NÓ: rag] Contexto recuperado ({len(contexto)} chars)")
    except Exception as e:
        print(f"[NÓ: rag] Erro ao buscar contexto: {e}")
        contexto = ""

    return {
        **state,
        "contexto_rag": contexto,
    }


def no_triagem(state: BluaState) -> BluaState:
    """
    Nó de triagem — coleta sintomas e avalia urgência.
    """
    print("[NÓ: triagem] Executando triagem...")

    resultado = agente_triagem(
        mensagem=state["mensagem_atual"],
        historico=state["historico"],
        contexto_rag=state["contexto_rag"],
    )

    # Verifica se o agente detectou red flag
    if resultado.get("escalada_necessaria") or resultado.get("red_flag_detectada"):
        print("[NÓ: triagem] Red flag detectada pelo LLM → escalada")
        return {
            **state,
            "red_flag_detectada": True,
            "proxima_acao": "escalada",
            "sintomas_coletados": resultado.get("sintomas_coletados", []),
            "resposta_final": resultado.get("mensagem_usuario", ""),
            "agente_usado": "triagem→escalada",
        }

    return {
        **state,
        "sintomas_coletados": resultado.get("sintomas_coletados", []),
        "urgencia": resultado.get("urgencia", "rotina"),
        "resposta_final": resultado.get("mensagem_usuario", ""),
        "agente_usado": "triagem",
        "proxima_acao": "fim",
    }


def no_prescricao(state: BluaState) -> BluaState:
    """
    Nó de prescrição — sugere rascunho para revisão médica.
    """
    print("[NÓ: prescrição] Executando prescrição...")

    historico_paciente = {}
    if state.get("paciente_id"):
        from src.tools.consultar_historico_paciente import consultar_historico_paciente
        historico_paciente = consultar_historico_paciente(state["paciente_id"])

    resultado = agente_prescricao(
        mensagem=state["mensagem_atual"],
        historico_paciente=historico_paciente,
        historico=state["historico"],
    )

    return {
        **state,
        "resposta_final": resultado.get("mensagem_usuario", ""),
        "agente_usado": "prescricao",
        "proxima_acao": "fim",
    }


def no_escalada(state: BluaState) -> BluaState:
    """
    Nó de escalada — aciona protocolo de emergência.
    """
    print("[NÓ: escalada] Acionando escalada humana...")

    resultado = agente_escalada(
        motivo="red_flag_detectada",
        sintomas=state.get("sintomas_coletados", [state["mensagem_atual"]]),
    )

    return {
        **state,
        "escalada_ativada": True,
        "triagem_encerrada": True,
        "resposta_final": resultado.get("mensagem_usuario", ""),
        "agente_usado": "escalada",
        "proxima_acao": "fim",
    }


def no_out_of_scope(state: BluaState) -> BluaState:
    """
    Nó para mensagens fora do escopo.
    """
    print("[NÓ: out_of_scope] Mensagem fora do escopo")

    return {
        **state,
        "resposta_final": (
            "Olá! Sou o BluaAssistente da Care Plus. "
            "Posso te ajudar com triagem de sintomas, informações de saúde "
            "e agendamento de teleconsultas. Como posso te ajudar hoje?"
        ),
        "agente_usado": "out_of_scope",
        "proxima_acao": "fim",
    }