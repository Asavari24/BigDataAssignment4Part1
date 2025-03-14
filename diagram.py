from diagrams import Diagram, Cluster
from diagrams.onprem.client import User
from diagrams.programming.framework import FastAPI
from diagrams.onprem.container import Docker
from diagrams.onprem.network import Nginx
from diagrams.aws.storage import S3  # Alternative for AWS S3
from diagrams.onprem.database import PostgreSQL  # Alternative for Redis
from diagrams.onprem.compute import Server  # Alternative for LLM API
from diagrams.generic.device import Mobile  # Alternative for Streamlit UI

with Diagram("PDF AI Assistant Architecture", show=True):
    
    user = User("User")

    with Cluster("Frontend"):
        streamlit_ui = Mobile("Streamlit UI")  # Using Mobile as an alternative UI representation

    with Cluster("Backend"):
        fastapi = FastAPI("FastAPI Backend")
        redis = PostgreSQL("Cache System")  # Using PostgreSQL as alternative for Redis
        s3 = S3("AWS S3 Storage")  # AWS S3 Storage alternative

    with Cluster("LLM Integration"):
        llm_api = Server("LLM API")  # Use Server as LLM API representation
    
    with Cluster("Deployment"):
        docker = Docker("Docker Container")
        github_pages = Nginx("GitHub Pages")

    user >> streamlit_ui >> fastapi
    fastapi >> [redis, s3, llm_api]
    docker >> [fastapi, streamlit_ui]
    github_pages >> streamlit_ui
