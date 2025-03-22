import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
import os
from datetime import datetime
import seaborn as sns
import matplotlib.pyplot as plt

########## DATA

script_path = os.path.dirname(os.path.abspath(__file__))
dim_members_path = os.path.join(script_path, "../../data2/synthetic/dim_members.csv")
dim_clinicians_path = os.path.join(script_path, "../../data2/synthetic/dim_clinicians.csv")
dim_biomarkers_path = os.path.join(script_path, "../../data2/synthetic/dim_biomarkers.csv")
fact_exmaniations_path = os.path.join(script_path, "../../data2/synthetic/fact_examinations.csv")
fact_data_collected_path = os.path.join(script_path, "../../data2/synthetic/fact_data_collected.csv")
fact_research_results_path = os.path.join(script_path, "../../data2/synthetic/fact_research_results.csv")

df_members = pd.read_csv(dim_members_path)
df_examinations = pd.read_csv(fact_exmaniations_path)
df_biomarkers = pd.read_csv(dim_biomarkers_path)
df_data_collected = pd.read_csv(fact_data_collected_path)
df_clinicians = pd.read_csv(dim_clinicians_path)
df_research_results = pd.read_csv(fact_research_results_path)

df_data = (df_data_collected
    .merge(df_examinations[['Examination_ID', 'Member_ID', 'Examination_Date', "Clinician_ID"]],
           on='Examination_ID', how='left')
    .merge(df_members[['Member_ID', 'Full_Name']],
           on='Member_ID', how='left')
    .merge(df_biomarkers[['Biomarker_ID', 'Biomarker_Name', 'Unit_Measurement']],
           on='Biomarker_ID', how='left'))

# Reorder columns
df_data = df_data.loc[:, ["Examination_Date", "Member_ID", "Full_Name", "Biomarker_Name", "Value", "Unit_Measurement", "Biomarker_ID", "Examination_ID", "Clinician_ID"]]

# Preprocessing
df_data['Examination_Date'] = pd.to_datetime(df_data['Examination_Date'])

########## APP
st.title("🔬 Population Research")
st.markdown("### Biomarker Analysis for Research")

# Create tabs for different research views
tab1, tab2 = st.tabs(["Correlation Analysis", "Biomarker Distributions"])

with tab1:
    st.subheader("Biomarker Correlation Matrix")

    # For each member, get their most recent examination
    member_latest_exams = df_data.sort_values('Examination_Date').groupby('Member_ID').last()['Examination_ID'].reset_index()
    latest_data = df_data[df_data['Examination_ID'].isin(member_latest_exams['Examination_ID'])]

    pivot_data = latest_data.pivot_table(
        index='Member_ID',
        columns='Biomarker_Name',
        values='Value',
        aggfunc='mean'  # in case of duplicates
    )
    correlation_matrix = pivot_data.corr()

    with st.expander("View Correlation Matrix Data"):
        st.write(correlation_matrix)

    fig = px.imshow(
        correlation_matrix,
        text_auto='.2f',
        aspect="auto",
        color_continuous_scale='Blues',
        zmin=-1, zmax=1,
        title="Biomarker Correlation Matrix"
    )

    fig.update_layout(
        height=700,
        width=700,
        xaxis_title="Biomarker",
        yaxis_title="Biomarker",
    )

    st.plotly_chart(fig, use_container_width=True)

    # downloadable correlation data
    st.download_button(
        label="Download Correlation Matrix (CSV)",
        data=correlation_matrix.to_csv().encode('utf-8'),
        file_name='biomarker_correlation_matrix.csv',
        mime='text/csv',
    )

with tab2:
    st.subheader("Biomarker Distribution Analysis")

    # Create a navigation system for biomarker visualization (similar to patient_summary.py)
    # Create columns for the navigation controls
    col1, col2, col3 = st.columns([1, 10, 1])

    # Get all biomarkers
    all_biomarkers = df_biomarkers['Biomarker_ID'].tolist()

    # Get the current biomarker index (default to first biomarker)
    if 'current_biomarker_index_research' not in st.session_state:
        st.session_state.current_biomarker_index_research = 0

    # Previous button
    with col1:
        if st.button("◀"):
            st.session_state.current_biomarker_index_research = (st.session_state.current_biomarker_index_research - 1) % len(all_biomarkers)
            st.rerun()

    # Biomarker selector
    with col2:
        # Create a list of biomarker names
        biomarker_options = df_biomarkers["Biomarker_Name"].tolist()

        # Create the selector
        selected_option = st.selectbox(
            "Select biomarker to visualize:",
            biomarker_options,
            index=st.session_state.current_biomarker_index_research
        )

        # Update the current index based on selection
        st.session_state.current_biomarker_index_research = biomarker_options.index(selected_option)

    # Next button
    with col3:
        if st.button("▶"):
            st.session_state.current_biomarker_index_research = (st.session_state.current_biomarker_index_research + 1) % len(all_biomarkers)
            st.rerun()

    # Get the currently selected biomarker
    current_biomarker_name = biomarker_options[st.session_state.current_biomarker_index_research]
    current_biomarker_id = df_biomarkers[df_biomarkers["Biomarker_Name"] == current_biomarker_name]["Biomarker_ID"].values[0]
    current_biomarker_unit = df_biomarkers[df_biomarkers["Biomarker_ID"] == current_biomarker_id]["Unit_Measurement"].values[0]

    # Get data for the current biomarker
    biomarker_data = df_data[df_data["Biomarker_ID"] == current_biomarker_id]

    # Create visualization for the selected biomarker
    col1, col2 = st.columns(2)

    with col1:
        # Create histogram
        fig_hist = px.histogram(
            biomarker_data,
            x="Value",
            title=f"Distribution of {current_biomarker_name} ({current_biomarker_unit})",
            labels={"Value": f"Value ({current_biomarker_unit})"},
            color_discrete_sequence=['skyblue']
        )

        # Add reference lines for "healthy ranges" from research_results table
        biomarker_research = df_research_results[df_research_results["Biomarker_ID"] == current_biomarker_id]
        if len(biomarker_research) > 0:
            upper_limit = biomarker_research["Upper_Limit"].values[0]
            lower_limit = biomarker_research["Lower_Limit"].values[0]

            fig_hist.add_vline(x=upper_limit, line_dash="dash", line_color="red")
            fig_hist.add_vline(x=lower_limit, line_dash="dash", line_color="red")

        st.plotly_chart(fig_hist, use_container_width=True)

    with col2:
        # Create boxplot
        fig_box = go.Figure()

        fig_box.add_trace(go.Box(
            y=biomarker_data["Value"],
            name=current_biomarker_name,
            boxpoints='all',
            jitter=0.3,
            pointpos=-1.8,
            marker_color='skyblue',
            line_color='darkblue'
        ))

        # Add reference lines for upper and lower limits
        if len(biomarker_research) > 0:
            fig_box.add_shape(
                type="line",
                x0=-0.5, x1=0.5,
                y0=upper_limit, y1=upper_limit,
                line=dict(color="red", width=2, dash="dash"),
            )

            fig_box.add_shape(
                type="line",
                x0=-0.5, x1=0.5,
                y0=lower_limit, y1=lower_limit,
                line=dict(color="red", width=2, dash="dash"),
            )

            # Add annotations for the limits
            fig_box.add_annotation(
                x=0.5, y=upper_limit,
                text=f"Upper Limit: {upper_limit:.2f}",
                showarrow=False,
                xanchor="left",
                yanchor="bottom"
            )

            fig_box.add_annotation(
                x=0.5, y=lower_limit,
                text=f"Lower Limit: {lower_limit:.2f}",
                showarrow=False,
                xanchor="left",
                yanchor="top"
            )

        fig_box.update_layout(
            title=f"Boxplot of {current_biomarker_name} ({current_biomarker_unit})",
            yaxis_title=f"Value ({current_biomarker_unit})",
            height=400,
            margin=dict(l=20, r=20, t=50, b=20),
            xaxis=dict(
                tickmode='array',
                tickvals=[],
                ticktext=[]
            )
        )

        st.plotly_chart(fig_box, use_container_width=True)


    # Display statistics for the selected biomarker
    st.subheader(f"Statistics for {current_biomarker_name}")

    stats = biomarker_data["Value"].describe()

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Mean", f"{stats['mean']:.2f}")

    with col2:
        st.metric("Median", f"{stats['50%']:.2f}")

    with col3:
        st.metric("Standard Deviation", f"{stats['std']:.2f}")

    with col4:
        # Calculate percentage of values outside normal range
        if len(biomarker_research) > 0:
            abnormal_values = biomarker_data[(biomarker_data["Value"] > upper_limit) | (biomarker_data["Value"] < lower_limit)]
            abnormal_percentage = (len(abnormal_values) / len(biomarker_data)) * 100
            st.metric("Abnormal Values", f"{abnormal_percentage:.1f}%")
        else:
            st.metric("Abnormal Values", "No reference data")

    # Add detailed statistics table
    with st.expander("View Detailed Statistics"):
        st.dataframe(stats)

        # Add additional statistics
        if len(biomarker_research) > 0:
            st.markdown("### Reference Range Analysis")
            above_range = len(biomarker_data[biomarker_data["Value"] > upper_limit])
            below_range = len(biomarker_data[biomarker_data["Value"] < lower_limit])
            within_range = len(biomarker_data[(biomarker_data["Value"] <= upper_limit) & (biomarker_data["Value"] >= lower_limit)])

            st.markdown(f"- **Above Range**: {above_range} ({above_range/len(biomarker_data)*100:.1f}%)")
            st.markdown(f"- **Below Range**: {below_range} ({below_range/len(biomarker_data)*100:.1f}%)")
            st.markdown(f"- **Within Range**: {within_range} ({within_range/len(biomarker_data)*100:.1f}%)")
