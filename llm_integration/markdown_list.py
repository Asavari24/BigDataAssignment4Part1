import os
import boto3
from dotenv import load_dotenv
from pathlib import Path


def list_markdown_files(bucket_name):

    #load_dotenv()
    load_dotenv(r'C:\Users\Admin\Desktop\MS Data Architecture and Management\DAMG 7245 - Big Data Systems and Intelligence Analytics\Assignment 4 A\environment\access.env')

    #s3 = boto3.client('s3')
    s3 = boto3.client(
        's3',
        aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
        region_name=os.getenv('AWS_REGION')
    )

    response = s3.list_objects_v2(Bucket=bucket_name)
    
    markdown_files = []
    filter_string = 'PyMuPDF'
    if 'Contents' in response:
        for obj in response['Contents']:
            if obj['Key'].endswith('.md'):
                if filter_string is None or filter_string.lower() in obj['Key'].lower():
                    filename = obj['Key'].split('/')[-1]
                    path = Path(filename)
                    file_name = path.stem
                    markdown_files.append(file_name)
    
    return markdown_files