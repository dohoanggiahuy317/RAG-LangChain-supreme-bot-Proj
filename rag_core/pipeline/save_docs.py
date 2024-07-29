from utils.document_loader import load_docs_from_folder
from utils.text_split import text_split
from utils.vectorstore.faiss_vectorstore import faiss_vectorstore, faiss_combine
from utils.vectorstore.chroma_vectorstore import chroma_vectorstore
from utils.embedding import get_embedding

import logging

def save_embedding(folder_path, db_type="faiss", db_path=None):

    # Decide db-type
    if db_type == "faiss":
        vectorstore = faiss_vectorstore
    else:
        vectorstore = chroma_vectorstore

    if db_path == None:
        if db_type == "faiss":
            db_path = "./database/faiss_db"
        else:
            db_path = "./database/chroma_db"

    # Set up logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    # Load DOCX files from a folder
    documents = load_docs_from_folder(folder_path)
    texts = text_split(documents)

    # Load into database
    logging.info("Save documents to vector database")
    embedding = get_embedding()
    db = vectorstore(texts, embedding, db_path)
    logging.info("Sucessfully saved documents to vector database")

    return db, embedding


def combine_embedding(folder_path, db_type="faiss", db_path=None):

    # Decide db-type
    if db_path == None:
        if db_type == "faiss":
            db_path = "./database/faiss_db"
        else:
            db_path = "./database/chroma_db"

    # Set up logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    # Load DOCX files from a folder
    documents = load_docs_from_folder(folder_path)
    texts = text_split(documents)

    # Load into database
    logging.info("Save documents to vector database")
    embedding = get_embedding()
    
    if db_type == "faiss":
        logging.info("Loading new documents")
        new_db = faiss_vectorstore(texts, embedding, db_path, save_local=False)

        logging.info("Merging new documents")
        update_db = faiss_combine(new_db, embedding, db_path)
    else:
        logging.info("Loading new documents")
        new_db = chroma_vectorstore(texts, embedding, db_path, save_local=False)
    
    logging.info("Sucessfully updated documents to vector database")

    return update_db, embedding


# save_embedding("/Users/dohoanggiahuy/Documents/Recent_files/abovedata/scrape/data/cocacola/document_txt")