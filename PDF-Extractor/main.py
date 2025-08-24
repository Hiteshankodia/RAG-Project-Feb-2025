import streamlit as st
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
#for splitting the text 

import os
from langchain_google_genai import GoogleGenerativeAIEmbeddings
#Converting text to vectors by Google Embeddings 

import google.generativeai as genai
from langchain_qdrant import Qdrant
#Using the updated Qdrant package
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
import qdrant_client

load_dotenv()
os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


def get_pdf_text(pdf_docs):
    #Getting text from PDF's
    text=""
    for pdf in pdf_docs:
        pdf_reader= PdfReader(pdf)
        for page in pdf_reader.pages:
            text+= page.extract_text()
    return text


#Creating chunks of the text
def get_text_chunks(text):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=10000, chunk_overlap=1000)
    chunks = text_splitter.split_text(text)
    return chunks

#Now I am converting chunks of text to vectors or embeddings 
def get_vector_store(text_chunks):
    embeddings = GoogleGenerativeAIEmbeddings(model = "models/embedding-001")
    
    # Create a local Qdrant client
    client = qdrant_client.QdrantClient(path="./qdrant_db")
    
    # Create a unique collection name or use a fixed one
    collection_name = "pdf_documents"
    
    # Check if collection exists and recreate if needed
    collections = client.get_collections().collections
    collection_names = [collection.name for collection in collections]
    
    if collection_name in collection_names:
        client.delete_collection(collection_name)
    
    # Create a new vector store using the updated Qdrant integration
    vector_store = Qdrant.from_texts(
        texts=text_chunks,
        embeddings=embeddings,  # Now using 'embeddings' instead of 'embedding'
        location="./qdrant_db",
        collection_name=collection_name,
    )
    
    return vector_store


def get_conversational_chain():

    prompt_template = """
    Answer the question as detailed as possible from the provided context, make sure to provide all the details, if the answer is not in
    provided context just say, "answer is not available in the context", don't provide the wrong answer\n\n
    Context:\n {context}?\n
    Question: \n{question}\n

    Answer:
    """

    model = ChatGoogleGenerativeAI(model="gemini-pro",
                             temperature=0.3)

    prompt = PromptTemplate(template = prompt_template, input_variables = ["context", "question"])

    chain = load_qa_chain(model, chain_type="stuff", prompt=prompt)
    #stuff will do the internal text summarization
    return chain


def user_input(user_question):
    #Loading Embeddings 
    embeddings = GoogleGenerativeAIEmbeddings(model = "models/embedding-001")
    
    # Connect to the local Qdrant database with the updated API
    vector_store = Qdrant(
        client=qdrant_client.QdrantClient(path="./qdrant_db"),
        collection_name="pdf_documents",
        embeddings=embeddings,  # Using 'embeddings' instead of 'embedding_function'
    )

    #Searching the questions embedding in the vector store
    docs = vector_store.similarity_search(user_question)

    chain = get_conversational_chain()

    response = chain(
        {"input_documents":docs, "question": user_question}
        , return_only_outputs=True)

    print(response)
    st.write("Reply: ", response["output_text"])


def main():
    st.set_page_config("Chat with Multiple PDF")
    st.header("Chat with Multiple PDF using Gemini💡")

    user_question = st.text_input("Ask a Question from the PDF Files")

    if user_question:
        user_input(user_question)

    with st.sidebar:
        st.title("Menu:")
        pdf_docs = st.file_uploader("Upload your PDF Files and Click on the Submit & Process Button", accept_multiple_files=True)
        if st.button("Submit & Process"):
            with st.spinner("Processing..."):
                raw_text = get_pdf_text(pdf_docs)
                text_chunks = get_text_chunks(raw_text)
                get_vector_store(text_chunks)
                st.success("Done")


if __name__ == "__main__":
    main()