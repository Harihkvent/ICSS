import os
import fitz  # PyMuPDF
import numpy as np
import torch  # For cosine similarity
from flask import Flask, request, jsonify
from sentence_transformers import SentenceTransformer
import google.generativeai as genai  # Corrected Import
from flask_cors import CORS  # Import CORS

  # Enable CORS globally

# Configure Gemini API Key
GEMINI_API_KEY = "AIzaSyAu7wh4Bq-IiNEikk4tbZ4ygEh07pmLwwg"
genai.configure(api_key=GEMINI_API_KEY)

# Load Sentence Transformer Model
embedder = SentenceTransformer("all-MiniLM-L6-v2")

app = Flask(__name__)
CORS(app)

# Load PDF & Precompute Embeddings
def load_pdf_extract_text(pdf_path):
    """Extracts text from the given PDF file."""
    doc = fitz.open(pdf_path)
    text_chunks = [page.get_text("text") for page in doc]
    return text_chunks

# Store processed embeddings
pdf_path = r"C:\MINI-PROJECT\ICSS\ICSS.pdf"
text_chunks = load_pdf_extract_text(pdf_path)
chunk_embeddings = embedder.encode(text_chunks, convert_to_tensor=True)

def retrieve_relevant_chunks(user_query, top_k=3):
    """Finds the most relevant chunks based on cosine similarity."""
    query_embedding = embedder.encode(user_query, convert_to_tensor=True)
    similarities = torch.matmul(chunk_embeddings, query_embedding.T)  # Fixed similarity calculation
    top_indices = torch.argsort(similarities, descending=True)[:top_k]
    return " ".join([text_chunks[i] for i in top_indices])

def generate_gemini_response(user_query, retrieved_context):
    """Uses Gemini API to generate a response based on retrieved context."""
    prompt = f"""
    You are an intelligent assistant. Given the user query and relevant context, generate a helpful response.

    Context: {retrieved_context}
    User Query: {user_query}

    Response:
    """
    model = genai.GenerativeModel("gemini-pro")  # Corrected API call
    response = model.generate_content(prompt)
    return response.text if response else "No response from Gemini API."

@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.json
        if not data or "query" not in data:
            return jsonify({"response": "Invalid request!"}), 400  # Return error

        user_query = data["query"]
        print(f"Received query: {user_query}")  # Debugging log

        retrieved_context = retrieve_relevant_chunks(user_query)
        final_response = generate_gemini_response(user_query, retrieved_context)

        return jsonify({"response": final_response})

    except Exception as e:
        print(f"Error processing request: {e}")  # Log the error
        return jsonify({"response": "Server error!"}), 500

if __name__ == "__main__":
    app.run(debug=True)
