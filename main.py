from model import TaskAuditor, TermAuditor, Analyzer
from docx import Document
import plotly.graph_objects as go

import pandas as pd
import matplotlib.pyplot as plt

import streamlit as st
import time
from pre_process import task_prompt, learning_prompt, contractor_prompt
from utilities import extract_json,  get_amount

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
#
submit=st.button("Tell me about the docs")

auditor_contract = TermAuditor(contractor_prompt)
auditor_task = TaskAuditor(task_prompt)
analytics = Analyzer(learning_prompt)

if submit:
    data = []

    amount = []


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
        et = extract_json(response)
        data.append(pd.DataFrame(et))
        my_bar.progress((index + 1)/len(cost_df.index), text=progress_text_task)
        time.sleep(3)
    task_data = pd.concat(data, ignore_index=True)
    task_data['Amount'] = cost_df['Amount']
    st.write(pd.DataFrame(task_data))


    st.header('Analysis and :blue [Result] :sunglasses:', divider='rainbow')
    progress_analysis_task = "Analyzing..... Please wait."
    my_bar = st.progress(0, text=progress_analysis_task)

    evaluation = []

    for i, task in enumerate(cost_df['Task Description']):
        try:

            output = analytics.analyze(task)
            evaluation.append(output)
            my_bar.progress((i+1)/100, text=progress_analysis_task)
        except Exception as error:
            print("Oops! error at %s" % str(error))
            print(i, task)


    cost_df['evaluation'] = evaluation

    st.dataframe(cost_df)

    cost_df.to_json('data.json')
    st.title('Results Visualization')

    for index in cost_df.index:
        if 'planned' in cost_df.iloc[index]['Task Description'] or 'pre-approved' in cost_df.iloc[index]['Task Description']:
            amount.append(cost_df.iloc[index]['Amount'])
        else:
            amount.append(get_amount(cost_df.iloc[index]['evaluation']))
    cost_df['Cost-Audit'] = amount
    st.write(cost_df)
    # Create the figure and axis
    dda = cost_df[['Task Description', 'Cost-Audit', 'Amount']].set_index('Task Description')

    fig, ax = plt.subplots(figsize=(12, 6))

    # Configure the layout


    st.bar_chart(dda[['Cost-Audit', 'Amount']])


    # Load the data

    # Create the Plotly figure
    fig = go.Figure()
    fig.add_trace(go.Bar(x=dda.index, y=dda['Amount'], name='Amount', marker_color='blue'))
    fig.add_trace(go.Bar(x=dda.index, y=dda['Cost-Audit'], name='Cost-Audit', marker_color='red'))

    # Display the chart in Streamlit
    st.plotly_chart(fig, use_container_width=True)

    # view first 10 rows of melted data frame

    fig = go.Figure()
    fig.add_trace(go.Box(y=dda['Cost-Audit'], name="Cost-Audit", marker_color='indianred'))
    fig.add_trace(go.Box(y=dda['Amount'], name="Amount", marker_color='lightseagreen'))
    st.plotly_chart(fig, use_container_width=True)



    # Create the Streamlit app

    x = dda.index
    y = dda['Amount']
    y_err = dda['Amount'] - dda['Cost-Audit']
    # Create the line chart
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(x, y, label="Data")
    ax.fill_between(x, y - y_err, y + y_err, alpha=0.3, label="Error Region")
    plt.xticks(x, rotation=90)

    ax.set_ylabel("Value")
    ax.legend()

    # Display the chart in Streamlit
    st.pyplot(fig)

