# Define the root directory of your project
ROOT_DIR="."

# Export PYTHONPATH to include the root directory
export PYTHONPATH="$ROOT_DIR"

python3 rag_core/main.py \
    --question "What are Coca-Cola’s primary goals in its sustainability initiatives, and how are they measured?" \
    --compressor_type 1 \
    --db_path "./rag_core/database/cocacola/faiss_db"
