

import json
from typing import List, Dict
from llama_index.core import (
    GPTVectorStoreIndex,
    SimpleDirectoryReader,
    ServiceContext,
)
from llama_index.llms.ollama import Ollama
from llama_index.embeddings import HuggingFaceEmbedding
from transformers import AutoTokenizer, AutoModelForCausalLM

# Load the JSON data
def load_json_data(file_path: str) -> List[Dict]:
    with open(file_path, 'r') as f:
        data = json.load(f)
    return data

# Prepare documents for indexing
def prepare_documents(data: List[Dict]) -> List[str]:
    documents = []
    for item in data:
        doc = f"Title: {item['title']}\n"
        doc += f"Source: {item['source']}\n"
        doc += f"URL: {item['url']}\n"
        doc += f"Content: {item['text']}\n\n"
        documents.append(doc)
    return documents

# Setup RAG system
def setup_rag(documents: List[str], system_prompt: str):
    # Initialize embedding model (INSTRUCTOR-XL)
    embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")

    # Initialize LLM
    llm_predictor = Ollama(model="llama3", request_timeout=120.0)

    # Create ServiceContext
    service_context = ServiceContext.from_defaults(
        llm_predictor=llm_predictor,
        embed_model=embed_model,
    )

    # Create VectorStoreIndex
    index = GPTVectorStoreIndex.from_documents(
        documents, service_context=service_context
    )

    # Initialize BM25Retriever
    bm25_retriever = BM25Retriever.from_defaults(documents=documents)

    # Initialize SentenceTransformerRerank
    reranker = SentenceTransformerRerank(
        model_name="cross-encoder/ms-marco-MiniLM-L-6-v2",
        top_n=5,
    )

    # Create RetrieverQueryEngine
    query_engine = RetrieverQueryEngine.from_args(
        retriever=bm25_retriever,
        node_postprocessors=[reranker],
        service_context=service_context,
    )

    # Set system prompt
    query_engine.update_prompts({"system_prompt": system_prompt})

    return query_engine

# Main function
def main():
    json_file_path = "Data cleansing/Cleansed data/text/llamaindex_prepared_data.json"
    system_prompt = "You are a helpful assistant. Answer the user's questions based on the provided context."

    # Load and prepare data
    data = load_json_data(json_file_path)
    documents = prepare_documents(data)

    # Setup RAG system
    query_engine = setup_rag(documents, system_prompt)

    # Example usage
    while True:
        user_query = input("Enter your question (or 'quit' to exit): ")
        if user_query.lower() == 'quit':
            break
        response = query_engine.query(user_query)
        print(f"Answer: {response}")

if __name__ == "__main__":
    main()