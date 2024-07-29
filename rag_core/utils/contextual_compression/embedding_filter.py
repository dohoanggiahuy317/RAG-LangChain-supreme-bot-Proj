from langchain.retrievers.document_compressors import DocumentCompressorPipeline
from langchain_community.document_transformers import EmbeddingsRedundantFilter
from langchain_text_splitters import CharacterTextSplitter
from langchain.retrievers import ContextualCompressionRetriever
from langchain.retrievers.document_compressors import EmbeddingsFilter


def get_compressed_docs(question, embedding, retriever):
    splitter = CharacterTextSplitter(
                            chunk_size=300, 
                            chunk_overlap=0, 
                            separator=". ")
    
    redundant_filter = EmbeddingsRedundantFilter(embeddings=embedding)
    relevant_filter = EmbeddingsFilter(
                        embeddings=embedding, 
                        similarity_threshold=0.75)
    
    pipeline_compressor = DocumentCompressorPipeline(
        transformers=[splitter, redundant_filter, relevant_filter]
    )

    compression_retriever = ContextualCompressionRetriever(
        base_compressor=pipeline_compressor, base_retriever=retriever
    )

    compressed_docs = compression_retriever.invoke(question)
    return compressed_docs