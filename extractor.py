from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.

import streamlit as st
import os
import pathlib
import textwrap
from docx import Document


import google.generativeai as genai


os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


def get_gemini_response(input,doc, prompt):
    model = genai.GenerativeModel('models/gemini-pro')
    response = model.generate_content([input,doc, prompt])
    return response.text



def input_doc_setup(uploaded_file):
    # Check if a file has been uploaded
    if uploaded_file is not None:
        # Read the file into bytes
        bytes_data = uploaded_file.getvalue()

        doc_parts = [
            {
                "mime_type": uploaded_file.type,  # Get the mime type of the uploaded file
                "data": bytes_data
            }
        ]
        return doc_parts
    else:
        raise FileNotFoundError("No file uploaded")

st.set_page_config(page_title="Gemini Image Demo")

st.header("Gemini Application")
input=st.text_input("Input Prompt: ",key="input")
uploaded_file = st.file_uploader("Choose an docs...")



# Open the document
document = Document(uploaded_file)

# Extract the text from the document
text = '\n'.join([paragraph.text for paragraph in document.paragraphs])




submit=st.button("Tell me about the docs")

input_prompt = """
               You are an expert in understanding invoices.
               You will receive input docs as invoices &
               you will have to answer questions based on the input docs
               """

## If ask button is clicked

if submit:
    doc_data = text
    response=get_gemini_response(input_prompt,doc_data,input)
    st.subheader("The Response is")
    st.write(response)