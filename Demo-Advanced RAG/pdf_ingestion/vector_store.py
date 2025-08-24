from langchain_core.vectorstores import InMemoryVectorStore

def create_vector_store(embeddings, all_splits):
    print("Embeddings", embeddings)
    print("Creating In-Memory Vector Store...")
    vector_store = InMemoryVectorStore(embeddings)
    vector_store.add_documents(documents=all_splits)
    return vector_store

def search_vector_store(vector_store, query):
    return vector_store.similarity_search(query)
   