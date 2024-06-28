from dotenv import load_dotenv
from json_tools import extract_json,validate_json_with_model,model_to_json,json_to_pydantic
load_dotenv()  # take environment variables from .env.
from typing import List
import json
import streamlit as st
import os
import pathlib
import textwrap
from docx import Document

import pandas as pd

import google.generativeai as genai

from pydantic import BaseModel

os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


class TermBase(BaseModel):
    term: str
    amount: str
    condition: str




def get_gemini_response(doc, prompt):
    model = genai.GenerativeModel('models/gemini-pro')
    response = model.generate_content([doc, prompt])
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

st.set_page_config(page_title="Contract Task Evaluation Demo")

st.header("Contractor Analysis Application")
# input=st.text_input("Input Prompt: ",key="input")
uploaded_file = st.file_uploader("Choose an docs...")

json_model = model_to_json(TermBase(term='term1',
                                    amount = "USD 2,500",
                                    condition = ''

))


# Open the document
document = Document(uploaded_file)

# Extract the text from the document
text = '\n'.join([paragraph.text for paragraph in document.paragraphs])




submit=st.button("Tell me about the docs")

input_prompt = f"""
               You are an expert in understanding invoices.
               You will receive input docs as invoices &
               you will have to answer questions based on the input docs
               You will be provided with a contract text containing various terms and constraints for work execution (e.g., budget constraints, types of allowable work, etc.).
               Your task is to extract all key terms from the contract and structure them in a JSON format. 
               Terms may be related to different sections and subsections of the contract, which should be reflected in your JSON.
               Please provide a response in a structured JSON format that matches the following model: {json_model}
               
                             
               """


## If ask button is clicked

if submit:
    doc_data = text
    response=get_gemini_response(doc_data, input_prompt)
    st.subheader("The Response is")
    output = {}
    output['terms'] = response
    agg = json.loads(response)
    value = ""
    for k, v in agg.items():
        value = v.replace("JSON", "").replace("```", "").strip()
    st.write(value)
    datav = json.loads(f"[{value}]")
    df = pd.DataFrame(datav)
    st.dataframe(df)  # Same as st.write(df)
    # with open("terms2.json", "w") as file:
    #     # Write the entire list to the file
    #     json.dump(output, file)