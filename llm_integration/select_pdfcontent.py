import boto3
import os
from dotenv import load_dotenv


def get_s3_client():

    load_dotenv(r'C:\Users\Admin\Desktop\MS Data Architecture and Management\DAMG 7245 - Big Data Systems and Intelligence Analytics\Assignment 4 A\environment\access.env')

    s3 = boto3.client(
        's3',
        aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
        region_name=os.getenv('AWS_REGION')
    )

    return s3



def select_pdfcontent(bucket_name, markdown_key):

    try:
        s3_client = get_s3_client()
        response = s3_client.get_object(Bucket=bucket_name, Key=markdown_key)
        markdown_content = response['Body'].read().decode('utf-8')

        return markdown_content
    
    except Exception as e:
        print(f"Error retrieving markdown: {str(e)}")
