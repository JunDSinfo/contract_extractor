from dotenv import load_dotenv
import json
from json_tools import extract_json, validate_json_with_model, model_to_json, json_to_pydantic
import pandas as pd
import time
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
class TaskBase(BaseModel):
    task: str
    location: str
    duration: str
    note: str
json_model = model_to_json(TaskBase(task='',
                                    location = '',
                                    duration = '',
                                    note = ''
                                  ))


def get_gemini_response(input, doc, prompt):
    model = genai.GenerativeModel('models/gemini-pro')
    response = model.generate_content([input, doc, prompt])
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


st.set_page_config(page_title="Extract Contractor Demo")

st.header("Contractor Analysis Application")
input = st.text_input("Input Prompt: ", key="input")
uploaded_file = st.file_uploader("Choose a file")
if uploaded_file is not None:
#read csv
    cost_df =  pd.read_excel(uploaded_file, sheet_name= 'Sheet1')


# Open the document

# Extract the text from the document

submit = st.button("Tell me about the docs")

input_prompt = f"""
               You are an expert in understanding tasks.
               You will receive a list of task&
               you will have to answer questions based on the input docs
               You will be provided with a contract text containing various terms and constraints for work execution (e.g., budget constraints, types of allowable work, etc.).
               Your task is to extract all key terms from the contract and structure them in a JSON format.
               Please provide a response in a structured JSON format that matches the following model: {json_model}

               """

import numpy as np

class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return super(NpEncoder, self).default(obj)



if submit:
    data = []
    for index in cost_df.index:
        output = {}
        doc_data = cost_df.loc[index]['Task Description']
        st.write(doc_data)

        response = get_gemini_response(input_prompt, doc_data, input)

        st.subheader("The Response is")
        st.write(response)
        output['description'] = response
        st.write(f"cost: {cost_df.loc[index]['Amount']}")
        output['cost'] = cost_df.loc[index]['Amount']
        print(output)
        data.append(output)
        time.sleep(3)
    print(data)
    with open("output.json", "w") as file:
        # Write the entire list to the file
        json.dump(data, file, cls=NpEncoder)