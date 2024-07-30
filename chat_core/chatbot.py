from langchain_ollama import OllamaLLM

from chat_core.utils.get_history import get_runnable_history
from chat_core.utils.get_prompt import prompt_template

from rag_core.pipeline.load_retriever import load_retriever
from rag_core.pipeline.load_CCCompressor import load_CCCompressor
from rag_core.pipeline.get_LLM import format_docs

import argparse
import logging

# class args():
#     question = "What is Coca-Cola's value, mission, and vision?"
#     compressor_type = 1
#     db_type = "faiss"
#     db_path = "./rag_core/database/cocacola/faiss_db"


def main():

    # Parser for shell script
    parser = argparse.ArgumentParser(description='RAG Application')
    parser.add_argument('--question', type=str, help='User query')
    parser.add_argument('--compressor_type', type=int, help='type of retriever compressor')
    parser.add_argument('--db_type', type=str, default="faiss", help='type of vector database')
    parser.add_argument('--db_path', type=str, default="./rag_core/database/cocacola/faiss_db", help='path to database')
    args = parser.parse_args()

    # Set up logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    # Load neccessary components
    embedding, retriever = load_retriever(db_type = args.db_type, db_path = args.db_path)
    get_compressed_docs = load_CCCompressor( compressor_type = int(args.compressor_type))

    # Init model
    llm = OllamaLLM(model="llama3")

    # Ranking the documents
    logging.info("Getting compressed_docs")
    if int(args.compressor_type) == 3:
        compressed_docs = get_compressed_docs(args.question, embedding, retriever)
        
        # save_log(args.question + "\n\n" + pretty_print_docs(compressed_docs), "./rag_core/logs/compress_docs/3/compressed_docs.txt")
        # save_log(args.question + "\n\n" + "\n".join(list(map(lambda x: str(x.metadata["source"]), compressed_docs))), "./rag_core/logs/compress_docs/3/metadata.txt")
    else:
        llm = OllamaLLM(model="llama3")
        compressed_docs = get_compressed_docs(args.question, llm, retriever)

        # save_log(args.question + "\n\n" + pretty_print_docs(compressed_docs), f"./rag_core/logs/compress_docs/{str(args.compressor_type)}/compressed_docs.txt")
        # save_log(args.question + "\n\n" + "\n".join(list(map(lambda x: str(x.metadata["source"]), compressed_docs))), f"./rag_core/logs/compress_docs/{str(args.compressor_type)}/metadata.txt")

    # Get prompt for the question
    prompt = prompt_template()
    runnable = prompt | llm
    formatted_doc = format_docs(compressed_docs)

    # Get chat history
    runnable_with_history = get_runnable_history(runnable)

    response = runnable_with_history.invoke(
        {
            "question": args.question,
            "context": formatted_doc
        },
        config={"configurable": 
                {
                    "user_id": "123", 
                    "conversation_id": "1",
                }},
    )

    logging.info(f"RESPONSE -- \n {response} \n")
    return response


if __name__ == "__main__":
    main()