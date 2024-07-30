from langchain_ollama import OllamaLLM

from pipeline.load_retriever import load_retriever
from pipeline.load_CCCompressor import load_CCCompressor
from pipeline.get_LLM import get_LLM

from utils.contextual_compression.pretty_print import pretty_print_docs
from utils.save_log import save_log

import argparse
import logging

def main():

    # Parser for shell script
    parser = argparse.ArgumentParser(description='RAG Application')
    parser.add_argument('--question', type=str, help='User query')
    parser.add_argument('--compressor_type', type=int, help='type of retriever compressor')
    parser.add_argument('--db_type', type=str, default="faiss", help='type of vector database')
    parser.add_argument('--db_path', type=str, default="./rag_core/database/denison/faiss_db", help='path to database')
    args = parser.parse_args()

    # Set up logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


    # Load neccessary components
    embedding, retriever = load_retriever(db_type = args.db_type, db_path = args.db_path)
    get_compressed_docs = load_CCCompressor(compressor_type = int(args.compressor_type))
    
    # Ranking the documents
    logging.info("Getting compressed_docs")
    if int(args.compressor_type) == 3:
        compressed_docs = get_compressed_docs(args.question, embedding, retriever)
    else:
        llm = OllamaLLM(model="llama3")
        compressed_docs = get_compressed_docs(args.question, llm, retriever)

    # Get response
    rag_chain = get_LLM(compressed_docs)

    logging.info("Inferencing response...")
    response = rag_chain.invoke(args.question)

    # Log the response
    logging.info(f"RESPONSE -- \n {response} \n")

    # Save the answer log to txt file
    save_log(
        "QUESTION: " + args.question + "\n\n" + "-"*50 + "\n\n"
        "RESPONSE: " + response + "\n\n" + "-"*50 + "\n\n"
        "METADATA: \n" + "\n".join(list(map(lambda x: str(x.metadata["source"]), compressed_docs))) + "\n\n" + "-"*50 + "\n\n"
        "DOCUMENTS: \n" + pretty_print_docs(compressed_docs),
        f"./rag_core/logs/{str(args.db_type)}/{str(args.compressor_type)}/response.txt"
    )

    return response

# Run the main function
if __name__ == "__main__":   
    main()


