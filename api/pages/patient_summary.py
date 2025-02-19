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

# Get relevant biomarker data (excluding Data_Collected_ID, Medical_Device_ID)
df_biomarker_data = df_data_collected.columns[["Biomarker_ID", "Examination_ID", "Value"]]

### APP
st.title("⚕️ Member Summary")

# select a specific patient (search by name)
# TODO: change to select by patient ID in case duplicate names
member_name = st.text_input("Enter patient name:")

if member_name in df_members["Full_Name"].values:
    member_record = df_members__examinations[df_members__examinations["Full_Name"] == member_name]

    # Get member's most recent examination data
    if len(member_record) > 1:
        member_record = member_record[member_record["Examination_Date"] == member_record["Examination_Date"].max()]
    st.write(f"{member_name} most recent record: ", member_record)

    # GET all the biomarker data from the associated examination_ID and plot a boxplot for each biomarker
    examination_id = member_record["Examination_ID"].iloc[0]
    st.write(examination_id)

    # st.write(df_data_collected)

    member_data = df_data_collected[df_data_collected["Examination_ID"] == examination_id]
    st.write("Member data: ", member_data)

    # Create boxplots for all member values
    fig = go.Figure()

    # Add boxplots for all patients
    for biomarker in biomarkers:
        fig.add_trace(go.Box(
            y=df_data_collected[biomarker],
            name=biomarker,
            boxpoints=False
        ))

        # Display member's latest examination value
        fig.add_trace(go.Scatter(
            x=[biomarker],
            y=[member_data[biomarker]],
            mode='markers',
            name=f'{member_name} latest',
            marker=dict(size=10, color='red'),
            showlegend=False
        ))

    # Update layout
    fig.update_layout(
        title="Biomarker Distribution with Patient's Latest Values",
        yaxis_title="Value",
        height=600,
        showlegend=False,
        margin=dict(l=0, r=0, t=40, b=0)
    )

    st.plotly_chart(fig, use_container_width=True)
else:
    st.write(f"Patient {member_name} not found")

st.write("Member - Examinations data:", df_members__examinations)
# for most recent examination,
# show which biomarkers are out of range (green, orange, red)
