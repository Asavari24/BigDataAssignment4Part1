import pymupdf4llm
import fitz
import os
import pandas as pd
import boto3
from io import BytesIO
from dotenv import load_dotenv
import logging



def upload_file_to_s3(file_content, bucket_name, s3_path):

    #load_dotenv()
    load_dotenv(r'C:\Users\Admin\Desktop\MS Data Architecture and Management\DAMG 7245 - Big Data Systems and Intelligence Analytics\Assignment 4 A\environment\access.env')

    #s3 = boto3.client('s3')
    s3 = boto3.client(
        's3',
        aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
        region_name=os.getenv('AWS_REGION')
    )

    s3.upload_fileobj(file_content, bucket_name, s3_path)




def extract_and_save_images(file_stream, image_prefix, bucket_name):
#def extract_and_save_images(pdf_path, image_prefix, bucket_name):
    #os.makedirs(image_prefix, exist_ok=True)
    doc = fitz.open(stream=file_stream, filetype="pdf")
    #doc = fitz.open(pdf_path)
    image_map = {}
    
    for page_num in range(len(doc)):
        page = doc[page_num]
        images = page.get_images(full=True)
        
        for img_index, img in enumerate(images):
            xref = img[0]
            base_image = doc.extract_image(xref)
            
            image_bytes = base_image["image"]
            image_ext = base_image["ext"]
            
            image_filename = f"page{page_num + 1}_img{img_index + 1}.{image_ext}"
            #image_path = os.path.join(image_prefix, image_filename)
            s3_image_path = f"{image_prefix}{image_filename}"

            # Direct upload to S3
            upload_file_to_s3(BytesIO(image_bytes), bucket_name, s3_image_path)
            
            #with open(image_path, "wb") as img_file:
            #    img_file.write(image_bytes)
            
            if page_num not in image_map:
                image_map[page_num] = []
            image_map[page_num].append(image_filename)
    
    return image_map



def extract_and_save_tables(file_stream, table_prefix, bucket_name):
#def extract_and_save_tables(pdf_path, table_prefix, bucket_name):    
    #os.makedirs(table_dir, exist_ok=True)
    doc = fitz.open(stream=file_stream, filetype="pdf")
    #doc = fitz.open(pdf_path)
    table_map = {}
    
    for page_num in range(len(doc)):
        page = doc[page_num]
        tables = page.find_tables()  # Find tables on the page
        
        for table_index, table in enumerate(tables):
            # Convert table to DataFrame
            df = pd.DataFrame(table.extract())
            
            # Save table as CSV
            table_filename = f"page{page_num + 1}_table{table_index + 1}.csv"
            #table_path = os.path.join(table_dir, table_filename)
            s3_table_path = f"{table_prefix}{table_filename}"
            #df.to_csv(table_path, index=False)

            # Direct upload to S3
            csv_buffer = BytesIO()
            df.to_csv(csv_buffer, index=False)
            csv_buffer.seek(0)
            upload_file_to_s3(csv_buffer, bucket_name, s3_table_path)
            
            if page_num not in table_map:
                table_map[page_num] = []
            table_map[page_num].append(table_filename)
    
    return table_map





def upload_pdf(file_name, file_stream, bucket_name):
#def process_pdf_s3_upload(pdf_path, bucket_name):    
    
    # Convert bytes into a file-like object
    #doc = BytesIO(file_content)

    #pdf_name = Path(pdf_path).stem
    #file_name = 'Text PDF'
    parser_prefix = f"{file_name}/PyMuPDF"
    image_prefix = f"{parser_prefix}/images/"
    table_prefix = f"{parser_prefix}/tables/"
    markdown_path = f"{parser_prefix}/{file_name}.md"


    # Extract and save images and tables
    image_map = extract_and_save_images(file_stream, image_prefix, bucket_name)
    table_map = extract_and_save_tables(file_stream, table_prefix, bucket_name) 

    #image_map = extract_and_save_images(pdf_path, image_prefix, bucket_name)
    #table_map = extract_and_save_tables(pdf_path, table_prefix, bucket_name) 

    try:
        # Convert PDF to markdown
        doc = fitz.open(stream=file_stream, filetype="pdf")
        #doc = fitz.open(pdf_path)
        markdown_content = ""   

        for page_num in range(len(doc)):

            # Get page content
            page_text = pymupdf4llm.to_markdown(doc, pages=[page_num])
            #page_text = pymupdf4llm.to_markdown(pdf_path, pages=[page_num])

            # Insert image references
            if page_num in image_map:
                for img_filename in image_map[page_num]:
                    image_ref = f"\n\n![Image](./{image_prefix}/{img_filename})\n\n"
                    paragraphs = page_text.split('\n\n')
                    if len(paragraphs) > 1:
                        for i, para in enumerate(paragraphs):
                            if para.strip():
                                paragraphs.insert(i + 1, image_ref)
                                break
                        page_text = '\n\n'.join(paragraphs)
                    else:
                        page_text += image_ref

            # Insert table references
            if page_num in table_map:
                for table_filename in table_map[page_num]:
                    # Create markdown table reference
                    table_ref = f"\n\n[View Table: {table_filename}](./{table_prefix}/{table_filename})\n\n"
                    page_text += table_ref

            markdown_content += page_text + "\n\n"

        # Save the markdown file
        #Path(markdown_path).write_text(markdown_content, encoding="utf-8")

        # Upload markdown directly to S3
        markdown_buffer = BytesIO(markdown_content.encode("utf-8"))
        upload_file_to_s3(markdown_buffer, bucket_name, markdown_path)
        return markdown_path
    
    except Exception as e:
        logging.error(f"Error during PDF extraction: {str(e)}")    


# Usage
#pdf_path = r"C:\Users\Admin\Desktop\MS Data Architecture and Management\DAMG 7245 - Big Data Systems and Intelligence Analytics\Assignment 1\Images and Tables PDF.pdf"
#bucket_name = "bigdatasystems"

#process_pdf_s3_upload(pdf_path, bucket_name)