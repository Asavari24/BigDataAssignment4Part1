
summary: PDF AI Assistant
id: pdf-ai-assistant
categories: Data Engineering, Cloud, AWS, LLM
status: Published
authors: Hishita Thakkar
feedback link: https://github.com/Asavari24/BigDataAssignment4Part1/issues
# PDF AI Assistant - Codelab
**ID:** pdf-ai-assistant


## **Introduction**
### **What You’ll Build**
In this Codelab, you will learn how to set up and deploy a **PDF AI Assistant** that allows users to upload, summarize, and ask questions about PDF documents using Large Language Models (LLMs). The system is built with **FastAPI** for backend processing, **Streamlit** for frontend interaction, **LiteLLM** for LLM API management, and **Redis & S3** for caching and storage.

### **What You’ll Learn**
- How to integrate **FastAPI** with Streamlit.
- How to process PDFs and extract content.
- How to use **LiteLLM** to interact with different LLMs (GPT-4o, Claude, Gemini, DeepSeek, Grok).
- How to cache and store PDF data efficiently using Redis and AWS S3.
- How to deploy the entire system using **Docker Compose**.

### **Prerequisites**
- Basic understanding of Python & FastAPI.
- Experience with Streamlit for UI development.
- Docker & AWS setup knowledge.

---

## **Step 1: Clone the Repository**
First, clone the repository containing the project files.

```sh
 git clone https://github.com/your-repo/pdf-ai-assistant.git
 cd pdf-ai-assistant
```

---

## **Step 2: Setup the Environment**
Create a Python virtual environment and install dependencies.

```sh
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
pip install -r requirements.txt
```

Create a **.env** file with your API keys:
```sh
OPENAI_API_KEY=your_openai_api_key
GEMINI_API_KEY=your_gemini_api_key
AWS_ACCESS_KEY_ID=your_aws_access_key
AWS_SECRET_ACCESS_KEY=your_aws_secret_key
AWS_REGION=your_aws_region
```

---

## **Step 3: Backend Development (FastAPI)**
We developed a **FastAPI backend** with multiple endpoints for handling PDF processing and LLM interactions.

### **Key Backend Features:**
- **List Markdown Files**: Retrieve stored markdown file names from S3.
- **Select PDF Content**: Fetches parsed markdown from previously processed PDFs.
- **Upload PDF**: Uploads a new PDF, processes its content, extracts text, images, and tables, and stores it in S3.
- **Summarization API**: Calls the LiteLLM API to generate document summaries.
- **Q&A API**: Allows users to ask questions based on document context.
- **Pricing API**: Calculates and returns estimated cost based on LLM token usage.

### **Start the FastAPI Backend:**
```sh
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

Once running, visit `http://127.0.0.1:8000/docs` to explore API endpoints.

---

## **Step 4: Frontend Development (Streamlit)**
The **Streamlit UI** provides an interactive way to:
- Select and upload PDFs.
- Choose a preferred LLM model.
- View document summaries.
- Ask questions about the document.
- Display token usage and cost estimations.

### **Start the Streamlit Frontend:**
```sh
streamlit run app.py
```

The UI will open in your browser at `http://localhost:8501/`.

---

## **Step 5: LLM Integration with LiteLLM**
We integrated **LiteLLM** for seamless API access to multiple LLM providers. This module handles:
- **Model Selection**: GPT-4o, Claude, Gemini, DeepSeek, Grok.
- **API Calls**: Sending document context and user queries to the LLM.
- **Token Pricing Calculation**: Returns the cost estimate for each query.
- **Error Handling**: Handles API failures gracefully.

### **Example LLM Interaction Code:**
```python
from litellm import completion

def generate_summary(context, model_type):
    messages = [
        {"role": "assistant", "content": context},
        {"role": "user", "content": "Give a brief summary of the context provided."}
    ]
    return completion(model=model_type, messages=messages)
```

---

## **Step 6: Redis Caching for Performance Optimization**
We use **Redis** to store extracted PDF content and summaries, reducing redundant API calls and improving response time.

### **Start Redis Server:**
```sh
redis-server
```

### **Cache Handling Code in FastAPI:**
```python
from redis import Redis

redis_client = Redis(host='localhost', port=6379, db=0)
redis_client.set("pdf_content", extracted_text)
```

---

## **Step 7: Deployment with Docker Compose**
To deploy the entire system, use **Docker Compose**:

### **Docker Setup:**
1. Create a `Dockerfile` for the FastAPI backend and Streamlit frontend.
2. Define a `docker-compose.yml` to run both services along with Redis.

### **Build & Run Containers:**
```sh
docker-compose up --build
```

The application will be accessible at:
- **Streamlit UI:** `http://localhost:8501`
- **FastAPI Backend:** `http://localhost:8000/docs`

To stop the containers:
```sh
docker-compose down
```

---

## **Step 8: Key Takeaways**
✅ **FastAPI & Streamlit** integration for interactive document processing.

✅ **LiteLLM** for seamless interaction with multiple LLMs.

✅ **Redis caching** for optimized performance.

✅ **Docker-based deployment** for scalability.

✅ **AWS S3** storage for long-term file management.

---

## **Conclusion**
By completing this Codelab, you have successfully built an AI-powered PDF Assistant that enables users to process and interact with documents efficiently using LLMs. This project can be extended to support additional models, improved caching, and enterprise deployment strategies.

---

## **Resources**
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [LiteLLM API Docs](https://docs.litellm.ai/)
- [Docker Documentation](https://docs.docker.com/)

