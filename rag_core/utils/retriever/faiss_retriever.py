from langchain_community.vectorstores import FAISS

def faiss_retriever(embedding, db_path="./rag_core/database/faiss_db", search_type="similarity_score_threshold", score_threshold=0.5, k=5):
    db = FAISS.load_local(db_path, embedding, allow_dangerous_deserialization=True)
    
    retriever = db.as_retriever(
                            search_type=search_type, 
                            search_kwargs={
                                "score_threshold": score_threshold,
                                "k": k}
                            )
    
    return retriever