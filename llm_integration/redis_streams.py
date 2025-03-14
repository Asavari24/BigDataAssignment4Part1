from io import BytesIO
from fastapi.responses import JSONResponse
import fitz
import pymupdf4llm
from redis import Redis

# Initialize Redis connection
redis_client = Redis(host='localhost', port=6379, db=0)

def redis_files():

    # Check if PDF is cached
    if redis_client.exists("pdf_content"):

        # Extract text from PDF using PyMuPDF
        pdf_bytes = redis_client.get("pdf_content")

        # Create a BytesIO object for PyMuPDF
        file_stream = BytesIO(pdf_bytes)

        doc = fitz.open(stream=file_stream, filetype="pdf")
        #markdown_content = ""   

        for page_num in range(len(doc)):

            # Get page content
            page_text = pymupdf4llm.to_markdown(doc, pages=[page_num])

        # Prepare context for LiteLLM
        context = page_text


    # Check if Markdown is cached
    elif redis_client.exists("markdown_content"):

        # Retrieve Markdown text from Redis
        markdown_text = redis_client.get("markdown_content")

        # Prepare context for LiteLLM
        context = markdown_text.decode("utf-8")


    else:
        return JSONResponse(content={"error": "PDF or Markdown file not found"}, status_code=400)
    

    return context