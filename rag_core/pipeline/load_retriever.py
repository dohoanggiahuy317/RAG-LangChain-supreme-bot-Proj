from utils.embedding import get_embedding
from utils.retriever.faiss_retriever import faiss_retriever
from utils.retriever.chroma_retriever import chroma_retriever

import logging

def load_retriever(db_type = "faiss"):
    # Set up logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    # Get the embedding
    embedding = get_embedding()

    # Select the retriever
    logging.info(f"Load {db_type.upper()} retriever")
    if db_type == "faiss":
        retriever = faiss_retriever(embedding)
    else:
        retriever = chroma_retriever(embedding)
    
    return embedding, retriever