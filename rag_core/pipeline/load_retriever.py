from rag_core.utils.embedding import get_embedding
from rag_core.utils.retriever.faiss_retriever import faiss_retriever
from rag_core.utils.retriever.chroma_retriever import chroma_retriever

import logging

def load_retriever(db_type = "faiss", db_path="./rag_core/database/faiss_db"):
    # Set up logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    # Get the embedding
    embedding = get_embedding()

    # Select the retriever
    logging.info(f"Load {db_type.upper()} retriever")
    if db_type == "faiss":
        retriever = faiss_retriever(embedding, db_path=db_path)
    else:
        retriever = chroma_retriever(embedding, db_path=db_path)
    
    return embedding, retriever