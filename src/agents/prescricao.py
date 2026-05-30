"""
prescricao.py

Agente especializado em sugestão de prescrição remota.
Consulta histórico do paciente, verifica interações
e gera rascunho para revisão médica.

IMPORTANTE: nunca substitui o médico — gera apenas rascunho.
"""

import os
import json

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage

load_dotenv()

OLLAMA_API_KEY = os.getenv("OLLAMA_API_KEY")

PROMPT_PRESCRICAO = """
Você é o agente de PRESCRIÇÃO REMOTA do BluaDiagnostics (Care Plus).

Sua função exclusiva é:
1. Analisar o histórico clínico do paciente
2. Verificar interações medicamentosas
3. Gerar um RASCUNHO de prescrição para revisão do médico

REGRAS ABSOLUTAS:
- Você NUNCA prescreve — apenas SUGERE para revisão médica
- Toda sugestão deve ser aprovada por um médico (Human-in-the-Loop)
- Se houver interação grave → alerte imediatamente e não sugira
- NUNCA invente medicamentos ou doses não baseadas no histórico

FORMATO DE RESPOSTA (sempre JSON):
{
  "mensagem_usuario": "texto explicativo para o usuário",
  "rascunho_prescricao": {
    "medicamento": "nome",
    "dose_sugerida": "dose baseada no histórico",
    "frequencia": "frequência",
    "observacoes": "observações clínicas"
  },
  "interacao_detectada": true | false,
  "severidade_interacao": "nenhuma | leve | moderada | grave",
  "aprovacao_medica_necessaria": true,
  "alerta": "texto de alerta se houver interação grave"
}
"""


def agente_prescricao(
    mensagem: str,
    historico_paciente: dict = {},
    resultado_interacoes: dict = {},
    historico: list = [],
) -> dict:
    """
    Executa o agente de prescrição remota.

    Args:
        mensagem: solicitação do usuário
        historico_paciente: retorno da tool consultar_historico_paciente
        resultado_interacoes: retorno da tool verificar_interacoes_medicamentosas
        historico: histórico da conversa

    Returns:
        Dicionário com rascunho de prescrição para revisão médica
    """
    llm = ChatOpenAI(
        model="gpt-oss:20b-cloud",
        api_key=OLLAMA_API_KEY,
        base_url="https://ollama.com/v1",
        temperature=0.1,
        max_tokens=1024,
    )

    # Monta contexto com dados do paciente
    contexto_paciente = ""
    if historico_paciente:
        contexto_paciente = f"\n\n[Histórico do paciente]:\n{json.dumps(historico_paciente, ensure_ascii=False, indent=2)}"

    contexto_interacoes = ""
    if resultado_interacoes:
        contexto_interacoes = f"\n\n[Verificação de interações]:\n{json.dumps(resultado_interacoes, ensure_ascii=False, indent=2)}"

    mensagens = [
        SystemMessage(content=PROMPT_PRESCRICAO + contexto_paciente + contexto_interacoes)
    ]

    for msg in historico:
        if msg["role"] == "user":
            mensagens.append(HumanMessage(content=msg["content"]))
        else:
            from langchain_core.messages import AIMessage
            mensagens.append(AIMessage(content=msg["content"]))

    mensagens.append(HumanMessage(content=mensagem))

    try:
        resposta = llm.invoke(mensagens)
        conteudo = resposta.content

        try:
            conteudo_limpo = conteudo.strip()
            if "```json" in conteudo_limpo:
                conteudo_limpo = conteudo_limpo.split("```json")[1].split("```")[0]
            elif "```" in conteudo_limpo:
                conteudo_limpo = conteudo_limpo.split("```")[1].split("```")[0]

            resultado = json.loads(conteudo_limpo)
        except json.JSONDecodeError:
            resultado = {
                "mensagem_usuario": conteudo,
                "rascunho_prescricao": {},
                "interacao_detectada": False,
                "severidade_interacao": "nenhuma",
                "aprovacao_medica_necessaria": True,
                "alerta": "",
            }

    except Exception as e:
        resultado = {
            "mensagem_usuario": f"Erro ao processar prescrição. ({str(e)[:100]})",
            "rascunho_prescricao": {},
            "interacao_detectada": False,
            "severidade_interacao": "nenhuma",
            "aprovacao_medica_necessaria": True,
            "alerta": "",
        }

    return resultado