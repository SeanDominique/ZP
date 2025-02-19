import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
import os

########## DATA
df_members = pd.read_csv("data2/synthetic/dim_members.csv")
df_examinations = pd.read_csv("data2/synthetic/fact_examinations.csv")
df_biomarkers = pd.read_csv("data2/synthetic/dim_biomarkers.csv")
df_data_collected = pd.read_csv("data2/synthetic/fact_data_collected.csv")
df_clinicians = pd.read_csv("data2/synthetic/dim_clinicians.csv")

df_data = (df_data_collected
    .merge(df_examinations[['Examination_ID', 'Member_ID', 'Examination_Date', "Clinician_ID"]],
           on='Examination_ID', how='left')
    .merge(df_members[['Member_ID', 'Full_Name']],
           on='Member_ID', how='left')
    .merge(df_biomarkers[['Biomarker_ID', 'Biomarker_Name', 'Unit_Measurement']],
           on='Biomarker_ID', how='left'))

# Reorder columns
df_data= df_data.loc[:, ["Examination_Date", "Member_ID", "Full_Name", "Biomarker_Name", "Value", "Unit_Measurement", "Biomarker_ID", "Examination_ID", "Clinician_ID"]] # "DOB", "Sex", "Is_Active", "Registered_Date",

# st.write(df_members__examinations.groupby(by="Full_Name").count()) # -> any dupes??

# Preprocessing
df_data['Examination_Date'] = pd.to_datetime(df_data['Examination_Date'])
# TODO: turn all names into lowercase to simplify search



########## APP
st.title("⚕️ Member Summary")

col1, col2 = st.columns(2)

# select a specific patient (search by name)
# TODO: change to select by patient ID in case duplicate names
with col1:
    st.subheader("Member info")
    member_name = st.text_input("Enter member name:")

with col2:
    st.subheader("Clinician info")

    # TODO: select clinician to filter by based on login
    clinician_name = st.selectbox(
        "Which clinician are you?",
        df_clinicians["Full_Name"].values,
        index=None,
        placeholder="Select contact method...",
    )

if clinician_name:
    # TODO: filter my clinician_ID if clinician's have the same name
    clinician_id = df_clinicians[df_clinicians["Full_Name"] == clinician_name]["Clinician_ID"].iloc[0]
    df_data = df_data[df_data["Clinician_ID"] == clinician_id]

if member_name in df_members["Full_Name"].values:
    member_record = df_data[df_data["Full_Name"] == member_name]

    # Get member's most recent examination data
    if len(member_record) > 1:
        member_record = member_record[member_record["Examination_Date"] == member_record["Examination_Date"].max()]
    st.markdown(f"*{member_name}* most recent record: ")
    st.write(member_record)

    # GET all the biomarker data from the associated examination_ID and plot  for each biomarker

    # Create boxplots for all member values
    fig = go.Figure()

    biomarkers = df_biomarkers["Biomarker_ID"].to_list()
    for biomarker_ID in biomarkers:
        # Filter data for this biomarker
        biomarker_data = df_data[df_data["Biomarker_ID"] == biomarker_ID]

        fig.add_trace(go.Box(
            y=biomarker_data["Value"],
            name=biomarker_ID,
            boxpoints=False
        ))

        # Display member's latest examination value
        member_value = member_record.loc[member_record["Biomarker_ID"] == biomarker_ID, "Value"].values
        if len(member_value) > 0:  # if member has this biomarker
            fig.add_trace(go.Scatter(
                x=[biomarker_ID],
                y=[member_value[0]],
                mode='markers',
                name=f'{member_name} latest',
                marker=dict(size=10, color='red'),
                showlegend=False
            ))

    # Update layout
    fig.update_layout(
        title=f"Biomarker distribution of all members with {member_name}'s most recent measurement",
        yaxis_title="Value",
        height=600,
        showlegend=False,
        margin=dict(l=0, r=0, t=40, b=0)
    )

    st.plotly_chart(fig, use_container_width=True)
else:
    st.write(f"Patient {member_name} not found")
    st.write("All member data:", df_data)

# for most recent examination,
# show which biomarkers are out of range (green, orange, red)
