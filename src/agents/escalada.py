"""
escalada.py

Agente de escalada humana.
Acionado quando red flags são detectadas ou situações
estão fora do escopo do sistema.
"""

import os

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage

load_dotenv()

OLLAMA_API_KEY = os.getenv("OLLAMA_API_KEY")

PROMPT_ESCALADA = """
Você é o agente de ESCALADA HUMANA do BluaDiagnostics (Care Plus).

Você é acionado APENAS em situações críticas ou fora do escopo.

Sua função:
1. Informar o usuário com clareza sobre a gravidade da situação
2. Orientar contato imediato com serviços de emergência
3. Encerrar a triagem — não retome após escalada

MENSAGEM OBRIGATÓRIA para red flags absolutas:
"⚠️ ATENÇÃO: Os sintomas que você descreveu podem indicar uma situação
que precisa de avaliação médica IMEDIATA. Por favor, ligue agora para
o SAMU (192) ou vá ao pronto-socorro mais próximo. Não espere."

Seja direto, claro e empático. Não minimize. Não continue a triagem.
"""


def agente_escalada(motivo: str, sintomas: list = []) -> dict:
    """
    Executa o protocolo de escalada humana.

    Args:
        motivo: motivo da escalada (red_flag, out_of_scope, etc.)
        sintomas: lista de sintomas que motivaram a escalada

    Returns:
        Dicionário com mensagem de escalada e status
    """
    llm = ChatOpenAI(
        model="gpt-oss:20b-cloud",
        api_key=OLLAMA_API_KEY,
        base_url="https://ollama.com/v1",
        temperature=0.1,
        max_tokens=512,
    )

    contexto_sintomas = ""
    if sintomas:
        contexto_sintomas = f"\nSintomas relatados: {', '.join(sintomas)}"

    mensagem = f"Motivo da escalada: {motivo}{contexto_sintomas}"

    mensagens = [
        SystemMessage(content=PROMPT_ESCALADA),
        HumanMessage(content=mensagem),
    ]

    try:
        resposta = llm.invoke(mensagens)
        mensagem_escalada = resposta.content
    except Exception as e:
        # Fallback hardcoded para garantir segurança mesmo com falha do LLM
        mensagem_escalada = (
            "⚠️ ATENÇÃO: Os sintomas que você descreveu podem indicar uma situação "
            "que precisa de avaliação médica IMEDIATA. Por favor, ligue agora para "
            "o SAMU (192) ou vá ao pronto-socorro mais próximo. Não espere."
        )

    return {
        "status": "escalada_ativada",
        "motivo": motivo,
        "mensagem_usuario": mensagem_escalada,
        "contatos_emergencia": {
            "samu": "192",
            "bombeiros": "193",
            "teleconsulta_urgente": "App Blua → Teleconsulta → Urgente",
        },
        "triagem_encerrada": True,
    }