import streamlit as st
import requests


# Set FastAPI URL
API_BASE_URL = "http://127.0.0.1:8000"


st.title("PDF AI Assistant")

st.sidebar.title("Navigation")
page = st.sidebar.radio("Services", ["File Selection", "Model Selection and Responses"])

if page == "File Selection":

    st.subheader("Select an Input Source")

    input_source = st.selectbox('Select parsed PDF or upload new PDF', ["Upload a New PDF", "Select Previously Parsed PDF"])

    st.divider()

    if input_source == "Select Previously Parsed PDF":

        st.subheader("Select Previously Parsed PDF")

        response = requests.get(f"{API_BASE_URL}/list_markdown_files")
        markdown_files = response.json().get("files", [])   


        if markdown_files:
            selected_file = st.selectbox("Select a parsed file", markdown_files, index=None, placeholder="Select an option" )     
            params = {"filename": selected_file}

            if selected_file:
                st.info(f"Fetching {selected_file} for processing...")
                try:
                    response = requests.get(f"{API_BASE_URL}/select_pdfcontent", params=params)

                    if response.status_code == 200:
                        st.success("File fetched successfully!")
                except Exception as e:
                    st.error(f"Error during retrieving file: {str(e)}")
        else:
            st.write("No markdown files found.")



    elif input_source == "Upload a New PDF":

        st.subheader("Upload a New PDF")

        uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

        if st.button("Upload PDF file"):
            if input_source == "Upload a New PDF" and uploaded_file:
                st.info("Uploading PDF for processing...")
                files = {"file": uploaded_file}

                try:
                    response = requests.post(f"{API_BASE_URL}/upload_pdf", files=files)

                    if response.status_code == 200:
                        st.success("File uploaded and parsed successfully!")
                    else:
                        st.error(f"Error: {response.json()['detail']}")

                except Exception as e:
                    st.error(f"Error during PDF upload: {str(e)}")

else:

    st.subheader("Select a Large Language Model")

    model_options = ["GPT-4o", "Gemini-Flash", "DeepSeek", "Claude", "Grok"]
    selected_model = st.selectbox("Select a LLM to use", model_options, index=0)

    st.divider()

    st.subheader("Summary of the Document")

    if st.button("Get the Summary"):

        params = {"model_type":selected_model}
        response = requests.get(f"{API_BASE_URL}/summarize", params=params)

        st.write(response.json()['choices'][0]['message']['content'])
       
        input_tokens = response.json()['usage']['prompt_tokens']
        output_tokens = response.json()['usage']['completion_tokens']
    
        param = {'input_tokens': input_tokens, 'output_tokens': output_tokens, 'selected_model': selected_model}
        response = requests.get(f"{API_BASE_URL}/pricing", params=param)
    
        total = response.json().get('total_value')

        st.divider()
    
        st.write(f'Total Input Tokens: {input_tokens}')
        st.write(f'Total Output Tokens: {output_tokens}')
        st.write(f'Total Price of this Query: ${total}')


    st.subheader("Responses for Questions on Document")

    question = st.text_input("Ask a question about the document")

    if st.button("Get a Response") and question:

        params = {"question": question, "model_type": selected_model}
        response = requests.get(f"{API_BASE_URL}/ask_question", params=params)

        st.write(response.json()['choices'][0]['message']['content'])

        input_tokens = response.json()['usage']['prompt_tokens']
        output_tokens = response.json()['usage']['completion_tokens']
    
        param = {'input_tokens': input_tokens, 'output_tokens': output_tokens, 'selected_model': selected_model}
        response = requests.get(f"{API_BASE_URL}/pricing", params=param)
    
        total = response.json().get('total_value')

        st.divider()
    
        st.write(f'Total Input Tokens: {input_tokens}')
        st.write(f'Total Output Tokens: {output_tokens}')
        st.write(f'Total Price of this Query: ${total}')


