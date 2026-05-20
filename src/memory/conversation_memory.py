"""
conversation_memory.py

Memória conversacional simples para a Sprint 1 do BluaCare.

Responsável por:
- salvar mensagens da conversa
- recuperar histórico recente
- limpar memória
"""

from datetime import datetime

# memória em RAM (simples para PoC)
conversation_memory = []


def save_message(role: str, content: str) -> None:
    """
    Salva uma mensagem no histórico da conversa.

    Args:
        role: 'user', 'assistant' ou 'system'
        content: conteúdo da mensagem
    """

    conversation_memory.append({
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "role": role,
        "content": content
    })


def get_history(limit: int = 10) -> list:
    """
    Retorna as últimas mensagens da conversa.

    Args:
        limit: quantidade máxima de mensagens

    Returns:
        Lista com histórico recente
    """

    return conversation_memory[-limit:]


def clear_history() -> None:
    """
    Limpa completamente o histórico da conversa.
    """

    conversation_memory.clear()


def print_history() -> None:
    """
    Exibe o histórico formatado no terminal/notebook.
    """

    if not conversation_memory:
        print("Histórico vazio.")
        return

    print("\n===== HISTÓRICO DA CONVERSA =====\n")

    for msg in conversation_memory:
        print(f"[{msg['timestamp']}] {msg['role'].upper()}:")
        print(msg["content"])
        print("-" * 50)