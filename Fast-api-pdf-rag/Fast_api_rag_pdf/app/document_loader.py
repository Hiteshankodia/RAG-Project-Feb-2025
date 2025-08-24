from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

def load_and_split_pdf(file_path: str):
    print('Loading Documents!')
    loader = PyPDFLoader(file_path)
    docs = loader.load()

    print(len(docs))
    print(f"{docs[0].page_content[:200]}\n")
    print(docs[0].metadata)

    print('Recursive Character Text Splitter!')
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=10000, chunk_overlap=1000) #, add_start_index=True)
    all_splits = text_splitter.split_documents(docs)

    print(len(all_splits))
    return all_splits
