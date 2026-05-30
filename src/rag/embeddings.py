"""
embeddings.py

Configura o modelo de embeddings para transformar
texto em vetores numéricos.

Modelo: sentence-transformers/all-MiniLM-L6-v2
- 100% local, sem custo, sem envio de dados a servidores externos
- Alinhado com requisito de privacidade LGPD do Challenge
"""

from langchain_community.embeddings import HuggingFaceEmbeddings


def obter_embeddings() -> HuggingFaceEmbeddings:
    """
    Retorna o modelo de embeddings configurado.

    Usa sentence-transformers localmente — nenhum dado
    é enviado a APIs externas (conformidade LGPD).

    Returns:
        Instância de HuggingFaceEmbeddings pronta para uso
    """
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True},
    )
    print("✅ Embeddings configurados: all-MiniLM-L6-v2 (local)")
    return embeddings