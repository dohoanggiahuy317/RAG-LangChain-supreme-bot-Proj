# Define the root directory of your project
ROOT_DIR="."

# Export PYTHONPATH to include the root directory
export PYTHONPATH="$ROOT_DIR"

python3 chat_core/chatbot.py \
    --question "What are Coca-Cola\u2019s primary goals in its sustainability initiatives, and how are they measured?" \
    --compressor_type 1 \
    --db_path "./rag_core/database/cocacola/faiss_db" \
    --user_id "admin" \
    --conversation_id "2"

python3 chat_core/chatbot.py \
    --question "Can you summarize your history reponse in 1 sentence?" \
    --compressor_type 1 \
    --db_path "./rag_core/database/cocacola/faiss_db" \
    --user_id "admin" \
    --conversation_id "2"
