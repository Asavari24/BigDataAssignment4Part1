from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from llm_integration.markdown_list import list_markdown_files
from llm_integration.model_info import model_name, pricing
from llm_integration.redis_streams import redis_files
from llm_integration.select_pdfcontent import select_pdfcontent
import os
from io import BytesIO
from fastapi import FastAPI, File, Query, UploadFile, HTTPException
from llm_integration.upload_pdf import upload_pdf
from redis import Redis
from litellm import completion
from dotenv import load_dotenv


app = FastAPI()

bucket_name='bigdatasystems'

# Initialize Redis connection
redis_client = Redis(host='localhost', port=6379, db=0)

load_dotenv(r'C:\Users\Admin\Desktop\MS Data Architecture and Management\DAMG 7245 - Big Data Systems and Intelligence Analytics\Assignment 4 A\environment\access.env')


# Set API key directly
os.environ["OPENAI_API_KEY"] = os.getenv('OPENAI_API_KEY')
os.environ['DEEPSEEK_API_KEY'] = os.getenv('DEEPSEEK_API_KEY')
os.environ['GEMINI_API_KEY'] = os.getenv('GEMINI_API_KEY')
os.environ['ANTHROPIC_API_KEY'] = os.getenv('ANTHROPIC_API_KEY')
os.environ['XAI_API_KEY'] = os.getenv('XAI_API_KEY')




@app.get("/list_markdown_files")
async def list_markdown_files_api():

    bucket_name = 'bigdatasystems'

    # Call the function to list markdown files
    markdown_files = list_markdown_files(bucket_name)
    return JSONResponse(content={"files": markdown_files}, media_type="application/json")


@app.get("/select_pdfcontent")
def select_pdf(filename: str = Query(...)):

    try:
        file_path = f'{filename}/PyMuPDF/{filename}.md'
        file_content = select_pdfcontent(bucket_name, file_path)

        # Delete any existing cached file
        redis_client.delete("pdf_content", "markdown_content")

        # Save PDF to Redis cache
        redis_client.set("markdown_content", file_content)
    
        return f'{filename} file has been fetched'

    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="File not found in S3.")
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching file: {str(e)}")
    




@app.post("/upload_pdf")
async def pdf_upload(file: UploadFile = File(...)):

    # Define size limit (3MB in bytes)
    MAX_FILE_SIZE = 3 * 1024 * 1024

    pdf_name = file.filename

    if not pdf_name.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed.")


    try:
        # Read the uploaded file's content
        file_content = await file.read()

        #pdf_name = file.filename
        file_name = os.path.splitext(pdf_name)[0]
        

        if len(file_content) > MAX_FILE_SIZE:
            raise HTTPException(status_code=413, detail="File size exceeds the 3MB limit")
        
        
        # Save the md file to s3 location
        s3_path = upload_pdf(file_name, BytesIO(file_content), bucket_name)

        # Delete any existing cached file
        redis_client.delete("pdf_content", "markdown_content")

        # Save PDF to Redis cache
        redis_client.set("pdf_content", file_content)

        #file_url = process_pdf_s3_upload(parsed_content, file.filename)
        return {"message": "File uploaded successfully", "file_url": s3_path}
    

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")



@app.get("/summarize")
async def summarize(model_type: str = Query(...)):

    try:

        context = redis_files()
        
        model = model_name(model_type)

        messages = [
            {"role": "assistant", "content": context},
            {"role": "user", "content": "Give a brief summary of the context provided in under 16385 tokens."}
        ]

        # Use LiteLLM to answer the question
        response = completion(model=model, messages=messages) 

        # Convert the response to a JSON-serializable format
        json_response = jsonable_encoder(response)
        return JSONResponse(content=json_response)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error returning a response: {str(e)}")
    



@app.get("/ask_question")
async def ask_question(question: str = Query(...), model_type: str = Query(...)):

    try:
        context = redis_files()

        model = model_name(model_type)

        messages = [
            {"role": "assistant", "content": context},
            {"role": "user", "content": f'{question}. Give your response based solely on the context provided.'}
        ]

        # Use LiteLLM to answer the question
        response = completion(model=model, messages=messages) 

        # Convert the response to a JSON-serializable format
        json_response = jsonable_encoder(response)
        return JSONResponse(content=json_response)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error returning a response: {str(e)}")
    


@app.get("/pricing")
async def model_pricing(input_tokens: int, output_tokens: int, selected_model: str):

    total = pricing(selected_model, input_tokens, output_tokens)

    return JSONResponse(content={"total_value": total}, media_type="application/json")