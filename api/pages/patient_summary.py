import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
import os

# DATA
df_members = pd.read_csv("data2/synthetic/dim_members.csv")
df_fact_examinations = pd.read_csv("data2/synthetic/fact_examinations.csv")
df_data_collected = pd.read_csv("data2/synthetic/fact_data_collected.csv")

df_members__examinations = pd.merge(left=df_members, right=df_fact_examinations, on="Member_ID", how="outer").sort_values(by="Full_Name")

# st.write(df_members__examinations.groupby(by="Full_Name").count()) # -> any dupes??

# Preprocessing
df_members__examinations['Examination_Date'] = pd.to_datetime(df_members__examinations['Examination_Date'])
# TODO: turn all names into lowercase to simplify search

# Get list of biomarkers (excluding ID, Name, and Date columns)
biomarkers = df_data_collected.columns[3:].tolist()

### APP
st.title("⚕️ Patient Summary")

# select a specific patient (search by name)
# TODO: change to select by patient ID in case duplicate names
patient_name = st.text_input("Enter patient name:")

if patient_name in df_members["Full_Name"].values:
    # Get the patient's most recent data
    patient_record = df_members__examinations[df_members__examinations["Full_Name"] == patient_name]

    if len(patient_record) > 1:
        patient_record = patient_record[patient_record["Examination_Date"] == patient_record["Examination_Date"].max()]
    st.write(f"{patient_name} record: ", patient_record)

    examination_date = patient_record["Examination_Date"].iloc[0]
    st.write(examination_date)
    # TODO: latest_examination_date =


    # GET all the biomarker data from the associated examination_ID and plot a boxplot for each biomarker

    # patient_data = df_data_collected[df_data_collected['Name'] == patient_name]
    # latest_date = patient_data['Date'].max()
    # latest_data = patient_data[patient_data['Date'] == latest_date].iloc[0]

    # # Display patient info
    # st.write(f"Patient: {patient_name}")
    # st.write(f"Latest examination date: {latest_date.strftime('%Y-%m-%d')}")

    # # Create boxplot with patient's values
    # fig = go.Figure()

    # # Add boxplots for all patients
    # for biomarker in biomarkers:
    #     fig.add_trace(go.Box(
    #         y=df_data_collected[biomarker],
    #         name=biomarker,
    #         boxpoints=False
    #     ))

    #     # Add patient's latest value as a scatter point
    #     fig.add_trace(go.Scatter(
    #         x=[biomarker],
    #         y=[latest_data[biomarker]],
    #         mode='markers',
    #         name=f'{patient_name} latest',
    #         marker=dict(size=10, color='red'),
    #         showlegend=False
    #     ))

    # # Update layout
    # fig.update_layout(
    #     title="Biomarker Distribution with Patient's Latest Values",
    #     yaxis_title="Value",
    #     height=600,
    #     showlegend=False,
    #     margin=dict(l=0, r=0, t=40, b=0)
    # )

    # st.plotly_chart(fig, use_container_width=True)
else:
    st.write(f"Patient {patient_name} not found")

st.write(df_members__examinations)
# for most recent examination,
# show which biomarkers are out of range (green, orange, red)
