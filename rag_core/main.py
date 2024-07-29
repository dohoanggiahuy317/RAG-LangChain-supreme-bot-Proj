from langchain_ollama import OllamaLLM

from pipeline.load_retriever import load_retriever
from pipeline.load_CCCompressor import load_CCCompressor
from pipeline.get_LLM import get_LLM

from utils.contextual_compression.pretty_print import pretty_print_docs
from utils.save_log import save_log

import argparse
import logging

class args():
    question = "What are some of the key areas of focus in Coca-Cola's sustainability efforts?"
    compressor_type = 1
    db_type = "faiss"

def main():

    # # Parser for shell script
    # parser = argparse.ArgumentParser(description='RAG Application')
    # parser.add_argument('--question', type=str, help='User query')
    # parser.add_argument('--compressor_type', type=int, help='type of retriever compressor')
    # parser.add_argument('--db_type', type=str, default="faiss", help='type of vector database')
    # args = parser.parse_args()

    # Set up logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


    # Load neccessary components
    embedding, retriever = load_retriever(db_type = args.db_type)
    get_compressed_docs = load_CCCompressor( compressor_type = int(args.compressor_type))
    
    # Ranking the documents
    logging.info("Getting compressed_docs")
    if int(args.compressor_type) == 3:
        compressed_docs = get_compressed_docs(args.question, embedding, retriever)
        
        save_log(args.question + "\n\n" + pretty_print_docs(compressed_docs), "./logs/compress_docs/3/compressed_docs.txt")
        save_log(args.question + "\n\n" + "\n".join(list(map(lambda x: str(x.metadata["source"]), compressed_docs))), "./logs/compress_docs/3/metadata.txt")
    else:
        llm = OllamaLLM(model="llama3")
        compressed_docs = get_compressed_docs(args.question, llm, retriever)

        save_log(args.question + "\n\n" + pretty_print_docs(compressed_docs), f"./logs/compress_docs/{str(args.compressor_type)}/compressed_docs.txt")
        save_log(args.question + "\n\n" + "\n".join(list(map(lambda x: str(x.metadata["source"]), compressed_docs))), f"./logs/compress_docs/{str(args.compressor_type)}/metadata.txt")

    # Get response
    rag_chain = get_LLM(compressed_docs)

    logging.info("Inferencing response...")
    response = rag_chain.invoke(args.question)

    # Log the response
    logging.info(f"RESPONSE -- \n {response} \n")


    if str(args.db_type) == "faiss":        
        save_log(args.question + "\n\n" + response, f"./logs/faiss/{str(args.compressor_type)}/response.txt")
    else:
        save_log(args.question + "\n\n" + response, f"./logs/chroma/{str(args.compressor_type)}/response.txt")


    return response

# Run the main function
if __name__ == "__main__":   
    main()


