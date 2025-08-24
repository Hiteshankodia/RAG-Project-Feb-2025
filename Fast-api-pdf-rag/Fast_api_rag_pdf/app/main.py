from fastapi import FastAPI, File, UploadFile, HTTPException
from io import BytesIO
import os
from app.document_loader import load_and_split_pdf
from app.embeddings import create_embeddings
from app.vector_store import create_vector_store, search_vector_store
from app.schema import QueryRequest, QueryResponse
from app.conversation_chain import get_conversational_chain
from app.corrective_rag import correct_response_with_documents

app = FastAPI()


all_splits = []
vector_store = None
embeddings = None

@app.post("/upload_pdf/")
async def upload_pdf(file: UploadFile = File(...)):
    global all_splits, vector_store, embeddings
    
    # Save the uploaded PDF to a temporary location
    file_path = f"temp_{file.filename}"
    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())
    
    # Load and split the document
    all_splits = load_and_split_pdf(file_path)

    # Create embeddings
    embeddings = create_embeddings()

    # Create the vector store
    vector_store = create_vector_store(embeddings, all_splits)

    os.remove(file_path)  # Clean up temporary file
    
    return {"message": "PDF processed and vector store created successfully."}

@app.post("/ask_question/")
async def ask_question(query_request: QueryRequest):
    if not vector_store:
        raise HTTPException(status_code=400, detail="PDF has not been uploaded yet.")
    
    query = query_request.question
    
    # Search the vector store
    docs = search_vector_store(vector_store, query)
    # print('Result - ', results)
    # doc, score = results[0] if results else (None, None)

    # if not doc:
    #     raise HTTPException(status_code=404, detail="No relevant documents found.")
    print('docs') 
    print(docs)

    chain = get_conversational_chain()

    
    response = chain(
        {"input_documents":docs, "question": query}
        , return_only_outputs=True)

    print(response)
    result = response["output_text"]
    
    #Adding Corrective RAG Code. 

    corrected_result = correct_response_with_documents(initial_answer = result,docs = docs, query=query)

    return QueryResponse(answer=result , crag_answer = corrected_result)
