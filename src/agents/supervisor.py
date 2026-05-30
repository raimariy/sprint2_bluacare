"""
supervisor.py

Agente supervisor — cérebro do sistema.
Recebe a mensagem do usuário e decide qual agente acionar.

Fluxo:
  mensagem → supervisor → triagem | prescricao | escalada
"""

import os
import re

from dotenv import load_dotenv

from src.agents.triagem import agente_triagem
from src.agents.prescricao import agente_prescricao
from src.agents.escalada import agente_escalada
from src.rag.retriever import buscar_contexto

load_dotenv()

# Palavras-chave de red flag para detecção rápida (antes do LLM)
PALAVRAS_RED_FLAG = [
    r"dor.{0,20}peito.{0,30}(braço|mandíbula|costas)",
    r"(braço|mandíbula).{0,30}dor.{0,20}peito",
    r"falta de ar.{0,20}repous",
    r"spo2.{0,10}(8[0-9]|9[0-1])\b",
    r"não consigo (falar|respirar)",
    r"lado.{0,15}(rosto|face).{0,20}(caiu|caído|paralis)",
    r"perdi.{0,10}consciência|desmaiei",
    r"convuls",
]

# Palavras-chave para roteamento
PALAVRAS_PRESCRICAO = [
    "prescrição", "prescricao", "receita", "medicamento",
    "remédio", "remedinho", "posso tomar", "interação",
]

PALAVRAS_OUT_OF_SCOPE = [
    "dólar", "cotação", "futebol", "receita de bolo",
    "política", "e-mail", "emprego",
]


def detectar_red_flag(mensagem: str) -> bool:
    """Detecção rápida de red flags por palavras-chave."""
    mensagem_lower = mensagem.lower()
    for padrao in PALAVRAS_RED_FLAG:
        if re.search(padrao, mensagem_lower):
            return True
    return False


def detectar_intencao(mensagem: str) -> str:
    """
    Detecta a intenção da mensagem para roteamento.

    Returns:
        'triagem' | 'prescricao' | 'escalada' | 'out_of_scope'
    """
    mensagem_lower = mensagem.lower()

    # Red flag tem prioridade máxima
    if detectar_red_flag(mensagem):
        return "escalada"

    # Out of scope
    if any(p in mensagem_lower for p in PALAVRAS_OUT_OF_SCOPE):
        return "out_of_scope"

    # Prescrição
    if any(p in mensagem_lower for p in PALAVRAS_PRESCRICAO):
        return "prescricao"

    # Default: triagem
    return "triagem"


def supervisor(
    mensagem: str,
    historico: list = [],
    paciente_id: str = None,
    vector_store=None,
) -> dict:
    """
    Supervisor principal — roteia a mensagem para o agente correto.

    Args:
        mensagem: mensagem do usuário
        historico: histórico da conversa
        paciente_id: ID do beneficiário (se identificado)
        vector_store: instância do ChromaDB para RAG

    Returns:
        Dicionário com resposta do agente acionado e metadados
    """
    print(f"\n[SUPERVISOR] Mensagem recebida: {mensagem[:60]}...")

    # 1. Detecta intenção
    intencao = detectar_intencao(mensagem)
    print(f"[SUPERVISOR] Intenção detectada: {intencao}")

    # 2. Busca contexto RAG se disponível
    contexto_rag = ""
    if vector_store and intencao in ("triagem", "prescricao"):
        try:
            contexto_rag = buscar_contexto(mensagem, vector_store, k=2)
            if contexto_rag:
                print(f"[RAG] Contexto recuperado ({len(contexto_rag)} chars)")
        except Exception as e:
            print(f"[RAG] Erro ao buscar contexto: {e}")

    # 3. Roteia para o agente correto
    if intencao == "escalada":
        print("[SUPERVISOR] → Acionando agente de ESCALADA")
        resultado = agente_escalada(
            motivo="red_flag_detectada",
            sintomas=[mensagem],
        )
        agente_usado = "escalada"

    elif intencao == "prescricao":
        print("[SUPERVISOR] → Acionando agente de PRESCRIÇÃO")

        # Busca histórico do paciente se tiver ID
        historico_paciente = {}
        if paciente_id:
            from src.tools.consultar_historico_paciente import consultar_historico_paciente
            historico_paciente = consultar_historico_paciente(paciente_id)

        resultado = agente_prescricao(
            mensagem=mensagem,
            historico_paciente=historico_paciente,
            historico=historico,
        )
        agente_usado = "prescricao"

    elif intencao == "out_of_scope":
        print("[SUPERVISOR] → Out of scope detectado")
        resultado = {
            "mensagem_usuario": (
                "Olá! Sou o BluaDiagnostics, assistente de saúde da Care Plus. "
                "Posso te ajudar com triagem de sintomas, informações de saúde e "
                "agendamento de teleconsultas. Como posso te ajudar hoje?"
            ),
            "triagem_encerrada": False,
        }
        agente_usado = "out_of_scope"

    else:
        print("[SUPERVISOR] → Acionando agente de TRIAGEM")
        resultado = agente_triagem(
            mensagem=mensagem,
            historico=historico,
            contexto_rag=contexto_rag,
        )
        agente_usado = "triagem"

    # 4. Retorna resultado com metadados
    return {
        "agente_usado": agente_usado,
        "intencao_detectada": intencao,
        "contexto_rag_usado": bool(contexto_rag),
        "resultado": resultado,
    }