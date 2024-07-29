from langchain_community.vectorstores import FAISS

def faiss_vectorstore(texts, embedding, db_path="./rag_core/database/faiss_db", save_local = True):
    db = FAISS.from_documents(texts, embedding)
    if save_local:
        db.save_local(db_path)
    
    return db


def faiss_combine(new_db, embedding, db_path="./rag_core/database/faiss_db", save_local = True):
    current_db = FAISS.load_local(db_path, embedding, allow_dangerous_deserialization=True)
    current_db.merge_from(new_db)

    if save_local:
        current_db.save_local(db_path)
    
    return current_db



