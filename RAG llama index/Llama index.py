from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, StorageContext, load_index_from_storage
from llama_index.core.vector_stores import SimpleVectorStore

# Load documents from a directory
documents = SimpleDirectoryReader("Data cleansing/Cleansed data/text").load_data()

# Create a storage context with a simple vector store
storage_context = StorageContext.from_defaults(
    vector_store=SimpleVectorStore()
)

# Create a vector store index from the loaded documents
index = VectorStoreIndex.from_documents(documents, storage_context=storage_context)

# Save the index to disk
storage_context.persist(persist_dir="Vectorised_Index")

# Load the index from disk
storage_context = StorageContext.from_defaults(
    persist_dir="Vectorised_Index",
    vector_store=SimpleVectorStore()
)
index = load_index_from_storage(storage_context=storage_context)

# Create a query engine
query_engine = index.as_query_engine(response_mode="tree_summarize")

# Query the index
response = query_engine.query("Hello. Pretend you are professor dumpster and respond in the way and tone he would. What is the meaning of life?")

print(response)
print(response.get_formatted_sources())