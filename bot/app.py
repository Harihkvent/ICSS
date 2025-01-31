# import os
# import requests
# from sklearn.feature_extraction.text import TfidfVectorizer
# from sklearn.metrics.pairwise import cosine_similarity
# import fitz  # PyMuPDF


# # Function to generate a response using an external LLM API
# def generate_response_from_api(prompt):
#     # Ensure your API key is set in environment variables
#     api_key = "9aRQppnnErYnxaZ35u7MgRw6YUTclJjeG27QAo7iEjU="  # Retrieve API key from environment variables
#     if not api_key:
#         raise ValueError("No API key found in the environment variable API_KEY")
    
#     url = 'https://ollama.omniqai.work/api/generate'  # Update this with your actual LLM endpoint
#     headers = {
#         'apikey': api_key,
#         'Content-Type': 'application/json'
#     }
#     payload = {
#         "model": "phi3",
#         "prompt": prompt,
#         "stream": False
#     }

#     try:
#         response = requests.post(url, headers=headers, json=payload, timeout=30)
#         if response.status_code == 200:
#             return response.json()
#         else:
#             print(f"Failed to get a valid response. Status code: {response.status_code}")
#             print(response.text)
#             return None
#     except requests.exceptions.RequestException as e:
#         print(f"Request failed: {e}")
#         return None


# # Step 1: Extract text from a PDF
# def extract_text_from_pdf(pdf_path):
#     text_chunks = []
#     with fitz.open(pdf_path) as pdf:
#         for page in pdf:
#             text = page.get_text()  # Extract text from the page
#             text_chunks.extend(text.split("\n\n"))  # Split into chunks
#     return [chunk.strip() for chunk in text_chunks if chunk.strip()]


# # Step 2: Retrieve the most relevant text chunk
# def retrieve_relevant_document(query, documents):
#     vectorizer = TfidfVectorizer()
#     doc_vectors = vectorizer.fit_transform(documents)
#     query_vector = vectorizer.transform([query])
#     similarities = cosine_similarity(query_vector, doc_vectors).flatten()
#     most_similar_idx = similarities.argmax()
#     return documents[most_similar_idx], similarities[most_similar_idx]


# # Step 3: Generate a response based on the retrieved chunk and LLM API
# def generate_final_response(query, retrieved_chunk):
#     # Combine the query and the most relevant document chunk for the LLM API
#     prompt = f"You are a virtual assistent to me. consider the following data that i have provided use this data and : '{retrieved_chunk}', answer the question: '{query}' perfectly dont extend response just answer the query in simple words using the data provided."
#     answer = generate_response_from_api(prompt)
#     if isinstance(answer, dict) and 'response' in answer:
#         return answer['response']
#     return None



# # Step 4: Main program
# if __name__ == "__main__":
#     # Specify the path to your PDF file
#     pdf_path = "ICSS.pdf"  # Replace with your PDF file path
#     print("Loading knowledge base from PDF...")
#     knowledge_base = extract_text_from_pdf(pdf_path)

#     if not knowledge_base:
#         print("The PDF seems to be empty or unreadable!")
#         exit()

#     print("Knowledge base loaded. You can now ask questions.")

#     # Query-Response Loop
#     while True:
#         user_query = input("\nAsk a question (or type 'exit' to quit): ")
#         if user_query.lower() == "exit":
#             print("Goodbye!")
#             break

#         # Retrieve the most relevant document chunk from the knowledge base
#         document, similarity = retrieve_relevant_document(user_query, knowledge_base)
#         if similarity > 0.1:  # Set a relevance threshold
#             # Generate a more comprehensive response using the LLM
#             response = generate_final_response(user_query, document)
#         else:
#             response = "Sorry, I couldn't find a relevant answer in the knowledge base."

#         # Print the response from the LLM
#         if response:
#             print(response)




import os
import requests
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import fitz  # PyMuPDF


# Function to generate a response using Gemini API
def generate_response_from_gemini(prompt):
    api_key = os.getenv("GEMINI_API_KEY")  # Retrieve API key from environment variables
    if not api_key:
        raise ValueError("No Gemini API key found in the environment variable GEMINI_API_KEY")
    
    url = f'https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateText?key={api_key}'
    headers = {
        'Content-Type': 'application/json'
    }
    payload = {
        "prompt": {"text": prompt},
        "temperature": 0.7
    }

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        if response.status_code == 200:
            data = response.json()
            return data.get("candidates", [{}])[0].get("output", "No response generated.")
        else:
            print(f"Failed to get a valid response. Status code: {response.status_code}")
            print(response.text)
            return None
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return None


# Step 1: Extract text from a PDF
def extract_text_from_pdf(pdf_path):
    text_chunks = []
    with fitz.open(pdf_path) as pdf:
        for page in pdf:
            text = page.get_text()
            text_chunks.extend(text.split("\n\n"))
    return [chunk.strip() for chunk in text_chunks if chunk.strip()]


# Step 2: Retrieve the most relevant text chunk
def retrieve_relevant_document(query, documents):
    vectorizer = TfidfVectorizer()
    doc_vectors = vectorizer.fit_transform(documents)
    query_vector = vectorizer.transform([query])
    similarities = cosine_similarity(query_vector, doc_vectors).flatten()
    most_similar_idx = similarities.argmax()
    return documents[most_similar_idx], similarities[most_similar_idx]


# Step 3: Generate a response based on the retrieved chunk and Gemini API
def generate_final_response(query, retrieved_chunk):
    prompt = f"You are a virtual assistant. Consider the following data: '{retrieved_chunk}'. Answer the question: '{query}' concisely using the provided data."
    return generate_response_from_gemini(prompt)


# Step 4: Main program
if __name__ == "__main__":
    pdf_path = "ICSS.pdf"
    print("Loading knowledge base from PDF...")
    knowledge_base = extract_text_from_pdf(pdf_path)

    if not knowledge_base:
        print("The PDF seems to be empty or unreadable!")
        exit()

    print("Knowledge base loaded. You can now ask questions.")

    while True:
        user_query = input("\nAsk a question (or type 'exit' to quit): ")
        if user_query.lower() == "exit":
            print("Goodbye!")
            break

        document, similarity = retrieve_relevant_document(user_query, knowledge_base)
        if similarity > 0.1:
            response = generate_final_response(user_query, document)
        else:
            response = "Sorry, I couldn't find a relevant answer in the knowledge base."

        if response:
            print(response)
