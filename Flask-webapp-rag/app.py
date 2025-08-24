from flask import Flask, request, jsonify, render_template
import requests

app = Flask(__name__)

# FastAPI URLs
UPLOAD_PDF_URL = "http://127.0.0.1:8000/upload_pdf/"
ASK_QUESTION_URL = "http://127.0.0.1:8000/ask_question/"

# Route for the home page that shows the upload form and ask question form
@app.route('/')
def index():
    return render_template('index.html')

# Route for uploading PDF
@app.route('/upload_pdf', methods=['POST'])
def upload_pdf():
    # Expecting a file upload in the request
    file = request.files.get('pdf')
    
    if not file:
        return jsonify({"error": "No file provided"}), 400
    
    # Prepare the payload and send the request to FastAPI
    files = {'file': file}
    response = requests.post(UPLOAD_PDF_URL, files=files)

    if response.status_code == 200:
        return jsonify({"message": "File uploaded successfully"})
    else:
        return jsonify({"error": "Failed to upload file", "details": response.text}), response.status_code

# Route for asking a question
@app.route('/ask_question', methods=['POST'])
def ask_question():
    # Get the question from the JSON body
    data = request.get_json()
    question = data.get('question')

    if not question:
        return jsonify({"error": "No question provided"}), 400
    
    # Prepare the payload for asking the question
    payload = {"question": question}
    
    # Send the request to FastAPI
    response = requests.post(ASK_QUESTION_URL, json=payload)

    if response.status_code == 200:
        return jsonify({"answer": response.json()})
    else:
        return jsonify({"error": "Failed to get an answer", "details": response.text}), response.status_code

if __name__ == "__main__":
    app.run(debug=True)
