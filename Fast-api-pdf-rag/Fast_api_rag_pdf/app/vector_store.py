from langchain_core.vectorstores import InMemoryVectorStore
from app.config import settings

from langchain_community.retrievers import AzureAISearchRetriever
from langchain_community.vectorstores import AzureSearch
# def create_vector_store(embeddings, all_splits):
#     print("Creating In-Memory Vector Store...")
    
#     vector_store = InMemoryVectorStore(embeddings)
#     ids = vector_store.add_documents(documents=all_splits)
    
#     return vector_store

def create_vector_store(embeddings, all_splits):
    print("Creating In-Memory Vector Store...")
    
    vector_store: AzureSearch = AzureSearch(
        embedding_function=embeddings,
        azure_search_endpoint=settings.AZURE_SEARCH_SERVICE_ENDPOINT,
        azure_search_key=settings.AZURE_SEARCH_API_KEY,
        index_name="hitesh-vector-store",
    )
    ids = vector_store.add_documents(documents=all_splits)
    
    return vector_store


def search_vector_store(vector_store, query):
    return vector_store.similarity_search(query)
    # retriever = AzureAISearchRetriever(
    #     content_key="content",
    #     top_k=1,
    #     index_name="hitesh-vector-store",
    #     service_name=settings.AZURE_SEARCH_SERVICE_ENDPOINT,  # Pass the service endpoint
    #     api_key=settings.AZURE_SEARCH_API_KEY,  # Pass the Azure search API key
    #     api_version="2023-07-01-preview",  # Optional, set default version if required
    # )
    result = retriever.invoke(query)
    print("result")
    print(result)
    print(retriever)
    print("Retriever")
    return result