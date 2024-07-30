# Define the root directory of your project
ROOT_DIR="."

# Export PYTHONPATH to include the root directory
export PYTHONPATH="$ROOT_DIR"

python3 chat_core/chatbot.py \
    --question "Can you summarize what you just said in 1 sentence?" \
    --compressor_type 3 \
    --db_path "./rag_core/database/cocacola/faiss_db"
