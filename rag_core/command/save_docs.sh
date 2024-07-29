# Define the root directory of your project
ROOT_DIR="./rag_core"

# Export PYTHONPATH to include the root directory
export PYTHONPATH="$ROOT_DIR"

python3 rag_core/pipeline/save_docs.py