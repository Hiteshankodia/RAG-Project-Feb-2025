from flask import Flask, render_template, request, redirect, url_for, jsonify
import os
from pdf_ingestion.document_loaded import load_and_split_pdf
from pdf_ingestion.embedding import create_embeddings 
from pdf_ingestion.vector_store import create_vector_store, search_vector_store
from pdf_retriever.conversation_chain import get_conversational_chain
import asyncio
from pandas_agent.pandas_agent import execute_query
import re
import pandas as pd
from sql_agent.sql_agent import run_sql_agent


# Dummy global state (replace with real implementations)
all_splits = None
vector_store = None
embeddings = None


app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/document-rag')
def document_rag():
    # Add your document RAG logic here
    return render_template('document_rag.html')


@app.route('/upload_pdf', methods=['POST'])
def upload_pdf():
    print(" Document Uploading... !")
    global all_splits, vector_store, embeddings

    uploaded_file = request.files.get('document')
    if uploaded_file and uploaded_file.filename.endswith('.pdf'):
        file_path = f"temp_{uploaded_file.filename}"
        uploaded_file.save(file_path)

        all_splits = load_and_split_pdf(file_path)
        embeddings = create_embeddings()
        vector_store = create_vector_store(embeddings, all_splits)
        os.remove(file_path)
        print("Loaded Document Successfully!")

        # ✅ Redirect with uploaded flag
        return redirect(url_for('document_rag', uploaded='true'))

    return "Invalid file", 400




def format_bold_markdown(text):
    """
    Replace **text** with <strong>text</strong> for markdown-style bold
    """
    return re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', text)

@app.route('/ask_pdf_query', methods=['POST'])
def ask_pdf_query():
    global vector_store

    if not vector_store:
        return render_template('document_rag.html', response="Please upload a PDF first.", uploaded='false')

    query = request.form.get("query")

    if not query:
        return render_template('document_rag.html', response="Please enter a query.", uploaded='true')

    docs = search_vector_store(vector_store, query)
    chain = get_conversational_chain()
    response = chain(
        {"input_documents": docs, "question": query},
        return_only_outputs=True
    )

    result = response["output_text"]
    formatted_result = format_bold_markdown(result)

    return render_template('document_rag.html', response=formatted_result, uploaded='true')




import pandas as pd

@app.route('/sql-rag', methods=['GET', 'POST'])
def sql_rag():
    markdown = None
    preview_table = None

    # Load CSV file for preview
    try:
        df = pd.read_csv('static/salaries_2023.csv')
        preview_df = df.head(5)
        preview_table = preview_df.to_html(classes='table', index=False, border=0)
    except Exception as e:
        preview_table = f"<p></p>"

    if request.method == 'POST':
        question = request.form.get('query')
        response = run_sql_agent(question)

        # Extract only the output/result part
        if isinstance(response, dict):
            markdown = (
                response.get('output') or 
                response.get('result') or 
                response.get('answer') or 
                str(response)
            )
        else:
            markdown = str(response)

    return render_template('sql_rag.html', markdown=markdown, preview_table=preview_table)





@app.route('/pandas-rag', methods=['GET', 'POST'])
def pandas_rag():
    

    # Load the Excel file (you can cache this in memory if needed)
    df = pd.read_excel('data.xlsx')
    preview_table = df.head().to_html(classes='preview-table', index=False, border=0)
    print(preview_table)
    
    markdown_output = None

    if request.method == 'POST':
        input_text = request.form.get('text') or ""

        # Run sync function in async-friendly way
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        raw_output = loop.run_until_complete(asyncio.to_thread(execute_query, input_text))
        loop.close()

        # ✅ Extract only the string value from the dictionary
        markdown_output = raw_output.get('result') if isinstance(raw_output, dict) else str(raw_output)
        print(markdown_output)

    return render_template(
        'pandas_rag.html',
        markdown=markdown_output,
        preview_table=preview_table
    )



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
