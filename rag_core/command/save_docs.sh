# Define the root directory of your project
ROOT_DIR="."

# Export PYTHONPATH to include the root directory
export PYTHONPATH="$ROOT_DIR"

python3 rag_core/pipeline/save_docs.py \
    --docs_path "./web_scrape/data/hanu/document_txt" \
    --db_path "./rag_core/database/hanu/faiss_db"