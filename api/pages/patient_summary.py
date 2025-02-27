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
# Load research results for biomarker flagging
df_research_results = pd.read_csv("data2/synthetic/fact_research_results.csv")

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
with col1:
    # select a specific patient (search by name)
    # TODO: change to select by patient ID in case duplicate names
    st.subheader("Member info")
    member_name = st.text_input("Enter member name:")

with col2:
    # TODO: select clinician to filter by based on login
    st.subheader("Clinician info")
    clinician_name = st.selectbox(
        "Which clinician are you?",
        df_clinicians["Full_Name"].values,
        index=None,
        placeholder="Select contact method...",
    )

if clinician_name:
    # TODO: filter my clinician_ID if multiple clinicians have the same name
    clinician_id = df_clinicians[df_clinicians["Full_Name"] == clinician_name]["Clinician_ID"].iloc[0]
    df_data = df_data[df_data["Clinician_ID"] == clinician_id]

# for most recent examination,
# show which biomarkers are out of range (green, orange, red)
def label_biomarker_range(value, biomarker_id, df_research_results):
    """
    Label biomarker values as red, orange, or green based on research results boundaries
    - Red: Value is outside the upper or lower limits
    - Orange: Value is within 2 standard deviations of the boundaries
    - Green: Value is well within normal range
    """
    # Get research results for this biomarker
    biomarker_research = df_research_results[df_research_results["Biomarker_ID"] == biomarker_id]

    if len(biomarker_research) == 0:
        return "gray"  # No research data available

    upper_limit = biomarker_research["Upper_Limit"].values[0]
    lower_limit = biomarker_research["Lower_Limit"].values[0]

    # Calculate mean and standard deviation
    mean = (upper_limit + lower_limit) / 2
    std_dev = (upper_limit - lower_limit) / 4  # Assuming range covers roughly 4 std deviations

    # Define boundaries for orange zone (2 std dev from limits)
    orange_upper = upper_limit - std_dev * 0.5
    orange_lower = lower_limit + std_dev * 0.5

    # Determine color based on value
    if value > upper_limit or value < lower_limit:
        return "red"
    elif value > orange_upper or value < orange_lower:
        return "orange"
    else:
        return "green"

if member_name in df_members["Full_Name"].values:
    member_record = df_data[df_data["Full_Name"] == member_name]

    # Get member's most recent examination data
    if len(member_record) > 1:
        latest_date = member_record["Examination_Date"].max()
        member_record = member_record[member_record["Examination_Date"] == latest_date]
    st.markdown(f"*{member_name}* most recent record: ")
    st.write(member_record)

    # Create a dictionary to store biomarker flags
    biomarker_flags = {}
    biomarker_values = {}

    # Flag each biomarker in the member's latest record
    for _, row in member_record.iterrows():
        biomarker_id = row["Biomarker_ID"]
        value = row["Value"]
        flag = label_biomarker_range(value, biomarker_id, df_research_results)
        biomarker_flags[biomarker_id] = flag
        biomarker_values[biomarker_id] = value

    # Group biomarkers by flag color
    red_biomarkers = [b for b, flag in biomarker_flags.items() if flag == "red"]
    orange_biomarkers = [b for b, flag in biomarker_flags.items() if flag == "orange"]
    green_biomarkers = [b for b, flag in biomarker_flags.items() if flag == "green"]
    gray_biomarkers = [b for b, flag in biomarker_flags.items() if flag == "gray"]

    # Sort biomarkers by flag priority: red, orange, green, gray
    sorted_biomarkers = red_biomarkers + orange_biomarkers + green_biomarkers + gray_biomarkers

    # Display summary of flagged biomarkers
    st.subheader("Biomarker Status Summary")

    # Add toggle to show/hide biomarker lists
    show_biomarker_details = st.toggle("Show detailed biomarker lists", value=True)

    if show_biomarker_details:
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(f"🔴 **Critical** ({len(red_biomarkers)})")
            for bio in red_biomarkers:
                bio_info = df_biomarkers[df_biomarkers["Biomarker_ID"] == bio]
                bio_name = bio_info["Biomarker_Name"].values[0]
                unit = bio_info["Unit_Measurement"].values[0]
                st.markdown(f"- {bio_name}: {biomarker_values[bio]:.2f} {unit}")

        with col2:
            st.markdown(f"🟠 **Warning** ({len(orange_biomarkers)})")
            for bio in orange_biomarkers:
                bio_info = df_biomarkers[df_biomarkers["Biomarker_ID"] == bio]
                bio_name = bio_info["Biomarker_Name"].values[0]
                unit = bio_info["Unit_Measurement"].values[0]
                st.markdown(f"- {bio_name}: {biomarker_values[bio]:.2f} {unit}")

        with col3:
            st.markdown(f"🟢 **Normal** ({len(green_biomarkers)})")
            for bio in green_biomarkers:
                bio_info = df_biomarkers[df_biomarkers["Biomarker_ID"] == bio]
                bio_name = bio_info["Biomarker_Name"].values[0]
                unit = bio_info["Unit_Measurement"].values[0]
                st.markdown(f"- {bio_name}: {biomarker_values[bio]:.2f} {unit}")
    else:
        # Show just the counts when details are hidden
        st.markdown(f"🔴 **Critical**: {len(red_biomarkers)} | 🟠 **Warning**: {len(orange_biomarkers)} | 🟢 **Normal**: {len(green_biomarkers)}")

    # Create a navigation system for biomarker visualization
    st.subheader("Biomarker Visualization")

    # Create columns for the navigation controls
    col1, col2, col3 = st.columns([1, 10, 1])

    # Get the current biomarker index (default to first biomarker)
    if 'current_biomarker_index' not in st.session_state:
        st.session_state.current_biomarker_index = 0

    # Previous button
    with col1:
        if st.button("◀"):
            st.session_state.current_biomarker_index = (st.session_state.current_biomarker_index - 1) % len(sorted_biomarkers)
            st.rerun()

    # Biomarker selector
    with col2:
        # Create a list of biomarker names with their flag status
        biomarker_options = []
        for bio_id in sorted_biomarkers:
            bio_name = df_biomarkers[df_biomarkers["Biomarker_ID"] == bio_id]["Biomarker_Name"].values[0]
            flag = biomarker_flags[bio_id]
            # Add emoji based on flag
            if flag == "red":
                emoji = "🔴"
            elif flag == "orange":
                emoji = "🟠"
            elif flag == "green":
                emoji = "🟢"
            else:
                emoji = "⚪"
            biomarker_options.append(f"{emoji} {bio_name}")

        # Create the selector
        selected_option = st.selectbox(
            "Select biomarker to visualize:",
            biomarker_options,
            index=st.session_state.current_biomarker_index
        )

        # Update the current index based on selection
        st.session_state.current_biomarker_index = biomarker_options.index(selected_option)

    # Next button
    with col3:
        if st.button("▶"):
            st.session_state.current_biomarker_index = (st.session_state.current_biomarker_index + 1) % len(sorted_biomarkers)
            st.rerun()

    # Get the currently selected biomarker
    current_biomarker_id = sorted_biomarkers[st.session_state.current_biomarker_index]
    current_biomarker_name = df_biomarkers[df_biomarkers["Biomarker_ID"] == current_biomarker_id]["Biomarker_Name"].values[0]
    current_biomarker_unit = df_biomarkers[df_biomarkers["Biomarker_ID"] == current_biomarker_id]["Unit_Measurement"].values[0]
    current_flag = biomarker_flags[current_biomarker_id]

    # Create visualization for the selected biomarker
    fig = go.Figure()

    # Get data for the current biomarker
    biomarker_data = df_data[df_data["Biomarker_ID"] == current_biomarker_id]

    # Add boxplot for all members
    fig.add_trace(go.Box(
        y=biomarker_data["Value"],
        name=current_biomarker_name,
        boxpoints='outliers',
        marker_color='lightgray',
        line_color='darkgray'
    ))

    # Add the member's value with appropriate color
    member_value = member_record.loc[member_record["Biomarker_ID"] == current_biomarker_id, "Value"].values
    if len(member_value) > 0:
        # Map flag colors to actual colors for the plot
        color_map = {"red": "red", "orange": "orange", "green": "green", "gray": "gray"}

        fig.add_trace(go.Scatter(
            x=[current_biomarker_name],
            y=[member_value[0]],
            mode='markers',
            name=f'{member_name}',
            marker=dict(size=15, color=color_map[current_flag], line=dict(width=2, color='black')),
            showlegend=True
        ))

    # Get research results for reference lines
    biomarker_research = df_research_results[df_research_results["Biomarker_ID"] == current_biomarker_id]
    if len(biomarker_research) > 0:
        upper_limit = biomarker_research["Upper_Limit"].values[0]
        lower_limit = biomarker_research["Lower_Limit"].values[0]

        # Add reference lines for upper and lower limits
        fig.add_shape(
            type="line",
            x0=-0.5, x1=0.5,
            y0=upper_limit, y1=upper_limit,
            line=dict(color="red", width=2, dash="dash"),
        )

        fig.add_shape(
            type="line",
            x0=-0.5, x1=0.5,
            y0=lower_limit, y1=lower_limit,
            line=dict(color="red", width=2, dash="dash"),
        )

        # Add annotations for the limits
        fig.add_annotation(
            x=0.5, y=upper_limit,
            text=f"Upper Limit: {upper_limit:.2f}",
            showarrow=False,
            xanchor="left",
            yanchor="bottom"
        )

        fig.add_annotation(
            x=0.5, y=lower_limit,
            text=f"Lower Limit: {lower_limit:.2f}",
            showarrow=False,
            xanchor="left",
            yanchor="top"
        )

    # Update layout
    fig.update_layout(
        title=f"{current_biomarker_name} ({current_biomarker_unit})",
        yaxis_title=f"Value ({current_biomarker_unit})",
        height=500,
        margin=dict(l=20, r=20, t=50, b=20),
        xaxis=dict(
            tickmode='array',
            tickvals=[],
            ticktext=[]
        )
    )

    st.plotly_chart(fig, use_container_width=True)

    # Display additional information about the selected biomarker
    st.markdown(f"### {current_biomarker_name} Details")

    # Create columns for the details
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            label=f"Current Value ({current_biomarker_unit})",
            value=f"{member_value[0]:.2f}" if len(member_value) > 0 else "N/A"
        )

    with col2:
        if len(biomarker_research) > 0:
            st.metric(
                label="Normal Range",
                value=f"{lower_limit:.2f} - {upper_limit:.2f} {current_biomarker_unit}"
            )
        else:
            st.metric(
                label="Normal Range",
                value="No data available"
            )

    with col3:
        # Display status with appropriate emoji
        if current_flag == "red":
            status = "🔴 Critical"
        elif current_flag == "orange":
            status = "🟠 Warning"
        elif current_flag == "green":
            status = "🟢 Normal"
        else:
            status = "⚪ Unknown"

        st.metric(
            label="Status",
            value=status
        )

    # Add a detailed explanation of the flagging system
    with st.expander("About Biomarker Flagging"):
        st.markdown("""
        ### Biomarker Flagging System

        - 🔴 **Red (Critical)**: Values outside the normal range limits. Immediate attention may be required.
        - 🟠 **Orange (Warning)**: Values close to the boundaries of normal range. Monitor closely.
        - 🟢 **Green (Normal)**: Values well within the normal range.

        The normal ranges are based on research studies with statistical significance.
        """)
else:
    st.write(f"Patient {member_name} not found")
    st.write("All member data:", df_data)
