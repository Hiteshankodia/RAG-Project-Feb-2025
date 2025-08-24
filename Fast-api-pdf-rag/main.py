from fastapi import FastAPI
from pydantic import BaseModel
from app.azure_services import search_pdf, index_pdf_document
from app.pdf_processing import extract_text_from_pdf, get_embeddings

app = FastAPI()

class QueryRequest(BaseModel):
    query: str
    pdf_path: str  # Path to the PDF that needs to be indexed or queried

@app.post("/index_pdf/")
async def index_pdf(request: QueryRequest):
    """
    Endpoint to index a PDF by extracting text, generating embeddings, and adding to Azure Search index.
    """
    pdf_path = request.pdf_path
    text = extract_text_from_pdf(pdf_path)
    embedding = get_embeddings(text)
    index_pdf_document(pdf_path, text, embedding)
    return {"message": f"PDF '{pdf_path}' indexed successfully."}

@app.post("/search_pdf/")
async def search_pdf_endpoint(request: QueryRequest):
    """
    Endpoint to search for relevant content from indexed PDF.
    """
    query = request.query
    pdf_path = request.pdf_path
    result = search_pdf(query, pdf_path)
    return {"results": result}
