"""
chunking.py

Responsável por carregar os documentos da knowledge base
e dividi-los em chunks para indexação no RAG.

Estratégia: chunks de 300 tokens com overlap de 50.
"""

import os

from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document


# Caminho da base de conhecimento
KNOWLEDGE_BASE_PATH = os.path.join(
    os.path.dirname(__file__), "..", "..", "data", "knowledge_base"
)


def carregar_documentos(pasta: str = KNOWLEDGE_BASE_PATH) -> list[Document]:
    """
    Carrega todos os arquivos .md da pasta knowledge_base.

    Args:
        pasta: caminho para a pasta com os documentos

    Returns:
        Lista de Documents do LangChain
    """
    documentos = []
    pasta = os.path.abspath(pasta)

    if not os.path.exists(pasta):
        raise FileNotFoundError(f"Pasta não encontrada: {pasta}")

    for arquivo in os.listdir(pasta):
        if arquivo.endswith(".md"):
            caminho = os.path.join(pasta, arquivo)
            try:
                loader = TextLoader(caminho, encoding="utf-8")
                docs = loader.load()
                # adiciona metadado com nome do arquivo de origem
                for doc in docs:
                    doc.metadata["source"] = arquivo
                documentos.extend(docs)
                print(f"  ✅ Carregado: {arquivo}")
            except Exception as e:
                print(f"  ❌ Erro ao carregar {arquivo}: {e}")

    print(f"\nTotal: {len(documentos)} documento(s) carregado(s)")
    return documentos


def dividir_em_chunks(
    documentos: list[Document],
    chunk_size: int = 300,
    chunk_overlap: int = 50,
) -> list[Document]:
    """
    Divide os documentos em chunks menores para indexação.

    Args:
        documentos: lista de Documents carregados
        chunk_size: tamanho máximo de cada chunk (em caracteres)
        chunk_overlap: sobreposição entre chunks consecutivos

    Returns:
        Lista de chunks prontos para indexação
    """
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", ".", " "],
    )

    chunks = splitter.split_documents(documentos)
    print(f"Total: {len(chunks)} chunk(s) gerado(s) "
          f"(chunk_size={chunk_size}, overlap={chunk_overlap})")
    return chunks