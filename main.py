from model import TaskAuditor, TermAuditor, Analyzer
from docx import Document
import pandas as pd
import json
import streamlit as st
import os
import time
from pre_process import task_prompt, learning_prompt, contractor_prompt
from utilities import extract_json, validate_json_with_model, get_amount
from pre_process import TermBase, TaskBase

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
uploaded_file = st.file_uploader("Choose an docs...")
# Open the document
document = Document(uploaded_file)
# Extract the text from the document
text = '\n'.join([paragraph.text for paragraph in document.paragraphs])
cost_df = pd.DataFrame()

st.write(text)
uploaded_file = st.file_uploader("Choose a file")
if uploaded_file is not None:
#read csv
    cost_df =  pd.read_excel(uploaded_file, sheet_name= 'Sheet1')

st.write(cost_df)

submit=st.button("Tell me about the docs")

auditor_contract = TermAuditor(contractor_prompt)
auditor_task = TaskAuditor(task_prompt)
analytics = Analyzer(learning_prompt)

if submit:
    data = []
    progress_text_term = "Reading contract terms. Please wait."

    progress_bar = st.progress(0)
    response = auditor_contract.get_response(text)

    dt = extract_json(response)
    df = pd.DataFrame(dt)
    st.dataframe(df)

    progress_bar.progress(100, text=progress_text_term)
    progress_text_task = "Reading tasks. Please wait."
    my_bar = st.progress(0, text=progress_text_task)
    for index in cost_df.index:
        output = {}
        doc_data = cost_df.loc[index]['Task Description']
        response = auditor_task.get_response(doc_data)

        output['description'] = response
        # st.write(f"cost: {cost_df.loc[index]['Amount']}")
        output['cost'] = cost_df.loc[index]['Amount']
        data.append(output)
        time.sleep(3)
        my_bar.progress((index + 1)/len(cost_df.index), text=progress_text_task)
    st.write(pd.DataFrame(data))


    st.header('Analysis and :blue [Result] :sunglasses:', divider='rainbow')
    progress_analysis_task = "Analyzing..... Please wait."
    my_bar = st.progress(0, text=progress_analysis_task)

    evaluation = []
    # amount_audit = []
    for i, task in enumerate(cost_df['Task Description']):
        output = analytics.analyze(task)
        evaluation.append(output)
        # amount_audit.append(get_amount(output))
        my_bar.progress((i+1)/100, text=progress_analysis_task)

    df['evaluation'] = evaluation
    # df['amount audit'] = amount_audit

    st.dataframe(df)

