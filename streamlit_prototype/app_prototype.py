import streamlit as st
import requests

st.title("PDF AI Assistant")
backend_url = "http://localhost:8000"

model_options = ["GPT-4o", "Gemini-Flash", "DeepSeek", "Claude", "Grok"]
selected_model = st.selectbox("Select LLM", model_options, index=0)
model_key = selected_model.lower().replace(" ", "-")

st.header("Select Previously Parsed PDF")

# Handling backend connection errors
try:
    response = requests.get(f"{backend_url}/select_pdfcontent/", timeout=5)
    response.raise_for_status()  # Raise an error for bad responses (4xx, 5xx)
    parsed_pdfs = response.json().get("parsed_pdfs", [])
except requests.exceptions.ConnectionError:
    st.error("Could not connect to the backend. Ensure the server is running.")
    parsed_pdfs = []
except requests.exceptions.Timeout:
    st.error("Request timed out. Try again later.")
    parsed_pdfs = []
except requests.exceptions.RequestException as e:
    st.error(f"An error occurred: {e}")
    parsed_pdfs = []

# Select PDF from previously parsed ones
selected_pdf = st.selectbox("Choose a PDF", [pdf["id"] for pdf in parsed_pdfs] + ["Upload New PDF"])
if selected_pdf != "Upload New PDF":
    st.session_state["content"] = [pdf["content"] for pdf in parsed_pdfs if pdf["id"] == selected_pdf][0]

# File uploader for new PDF
uploaded_file = st.file_uploader("Or Upload a New PDF", type=["pdf"])
if uploaded_file:
    files = {"file": (uploaded_file.name, uploaded_file, "application/pdf")}
    response = requests.post(f"{backend_url}/upload-pdf/", files=files)
    if response.status_code == 200:
        text_content = response.json()["content"]
        st.session_state["content"] = text_content
        st.success("PDF uploaded and processed successfully!")
    else:
        st.error("Failed to process PDF.")

# Display extracted text and allow summarization & Q&A
if "content" in st.session_state:
    st.text_area("Extracted Text", st.session_state["content"], height=200)
    if st.button("Summarize Document"):
        response = requests.post(f"{backend_url}/summarize/", json={"content": st.session_state["content"], "model": model_key})
        st.subheader("Summary:")
        st.write(response.json()["summary"])
    
    question = st.text_input("Ask a question about the document")
    if st.button("Get Answer") and question:
        response = requests.post(f"{backend_url}/ask-question/", json={"content": st.session_state["content"], "question": question, "model": model_key})
        st.subheader("Answer:")
        st.write(response.json()["answer"])