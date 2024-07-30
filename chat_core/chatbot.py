from langchain_ollama import OllamaLLM

from chat_core.utils.get_history import get_runnable_history
from chat_core.utils.get_prompt import prompt_template

from rag_core.pipeline.load_retriever import load_retriever
from rag_core.pipeline.load_CCCompressor import load_CCCompressor
from rag_core.pipeline.get_LLM import format_docs
from rag_core.utils.save_log import add_log
from rag_core.utils.contextual_compression.pretty_print import pretty_print_docs

import argparse
import logging

def main():

    # Parser for shell script
    parser = argparse.ArgumentParser(description='RAG Application')
    parser.add_argument('--question', type=str, help='User query')
    parser.add_argument('--compressor_type', type=int, help='type of retriever compressor')
    parser.add_argument('--db_type', type=str, default="faiss", help='type of vector database')
    parser.add_argument('--db_path', type=str, default="./rag_core/database/cocacola/faiss_db", help='path to database')
    parser.add_argument('--user_id', type=str, help='user id')
    parser.add_argument('--conversation_id', type=str, help='conversation id')
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
                    "user_id": args.user_id, 
                    "conversation_id": args.conversation_id,
                }},
    )

    # Save the answer log to txt file
    add_log(
        "USER: " + args.question + "\n\n"
        "SYSTEM: " + response  + "\n\n" + "-"*50 + "\n",
        f"./chat_core/logs/{str(args.user_id)}-{args.conversation_id}/{str(args.db_type)}/{str(args.compressor_type)}/chat/response.txt"
    )

    add_log(
        "QUESTION: " + args.question + "\n\n" + "-"*50 + "\n\n"
        "RESPONSE: " + response + "\n\n" + "-"*50 + "\n\n"
        "METADATA: \n" + "\n".join(list(map(lambda x: str(x.metadata["source"]), compressed_docs))) + "\n\n" + "-"*50 + "\n\n"
        "DOCUMENTS: \n" + pretty_print_docs(compressed_docs) + "\n\n" + ("-"*50 + "\n" + "-"*50 + "\n" + "-"*50) + "\n",
        f"./chat_core/logs/{str(args.user_id)}-{args.conversation_id}/{str(args.db_type)}/{str(args.compressor_type)}/info/response.txt"
    )

    logging.info(f"RESPONSE -- \n {response} \n")
    return response


if __name__ == "__main__":
    main()