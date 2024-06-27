from dotenv import load_dotenv
from json_tools import extract_json,validate_json_with_model,model_to_json,json_to_pydantic
load_dotenv()  # take environment variables from .env.
from typing import List

import streamlit as st
import os
import pathlib
import textwrap
from docx import Document


import google.generativeai as genai

from pydantic import BaseModel

os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


class TermBase(BaseModel):
    term: str
    amount: str
    section: str
    subsection: str




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

st.header("Contractor Analysis Application")
input=st.text_input("Input Prompt: ",key="input")
uploaded_file = st.file_uploader("Choose an docs...")

json_model = model_to_json(TermBase(term='term1',
                                    amount = "USD 2,500",
                                    section = 'section',
                                    subsection = 'subsection'
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
               Example for Application of Multi-Factor Adjustments:
               Consider an urgent business requirement necessitates travel to New York City over New Year’s weekend, with flight booking required on a Friday night. If the base approved travel budget is $2,500, the applicable adjustments would be:	•	Night and Weekend Travel Multiplier: 1.1
	           Seasonal and Location Adjustment for New York during New Year: 1.2
               Urgency Multiplier for last-minute booking: 1.3
               The total allowable expense for this travel scenario would be $2,500 * 1.1 * 1.2 * 1.3 = $4,158.
               Terms may be related to different sections and subsections of the contract, which should be reflected in your JSON.
               Please provide a response in a structured JSON format that matches the following model: {json_model}
               
                             
               """


## If ask button is clicked

if submit:
    doc_data = text
    response=get_gemini_response(input_prompt,doc_data,input)
    st.subheader("The Response is")
    st.write(response)