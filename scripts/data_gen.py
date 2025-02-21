import numpy as np
import pandas as pd
import random
import os
import json
from datetime import datetime
from sklearn.preprocessing import StandardScaler
from faker import Faker
# import Biomarker
import matplotlib.pyplot as plt

### CONSTANTS
BIOMARKER_TO_DEVICE = {
    "BIO_8OH_DG": "DEV_LC_003",
    "BIO_ANTILDL": "DEV_ELISA_002",
    "BIO_COQ10": "DEV_LC_003",
    "BIO_SOD": "DEV_CC_001",
    "BIO_GPX": "DEV_CC_001",
    "BIO_ZN": "DEV_ICP_005",
    "BIO_CU": "DEV_ICP_005",
    "BIO_SE": "DEV_ICP_005",
    "BIO_HCY": "DEV_CC_001",
    "BIO_TAC": "DEV_CC_001",
    "BIO_DOP": "DEV_LC_003",
    "BIO_3_4DOPAC": "DEV_LC_003",
    "BIO_HVA": "DEV_HPLC_004",
    "BIO_MHPG": "DEV_HPLC_004",
    "BIO_VMA": "DEV_HPLC_004",
    "BIO_SER": "DEV_LC_003",
    "BIO_5_HIAA": "DEV_LC_003",
    "BIO_ADR": "DEV_HPLC_004",
    "BIO_NADR": "DEV_HPLC_004",
    "BIO_TP": "DEV_CC_001",
    "BIO_A1G": "DEV_CC_001",
    "BIO_A2G": "DEV_CC_001",
    "BIO_BG": "DEV_CC_001",
    "BIO_GG": "DEV_CC_001",
    "BIO_ALB": "DEV_CC_001",
    "BIO_CRP": "DEV_ELISA_002",
    "BIO_SUPAR": "DEV_ELISA_002",
    "BIO_HA": "DEV_ELISA_002"
}


# TODO: should pull this data from a database of researched biomarker data from research papers / clinicial studies
# Define realistic ranges for each biomarker (example ranges)
BIOMARKER_PARAMS = {
    # Oxidative biomarkers
    "BIO_8OH_DG": {"mean": 2.5, "std_dev": 0.8},          # 8OH-DG in ug/L
    "BIO_ANTILDL": {"mean": 5.0, "std_dev": 1.5},           # Anti-LDL ox-IgG in mg/dL
    "BIO_COQ10": {"mean": 1.5, "std_dev": 0.4},             # Coenzyme Q10 in ug/mL
    "BIO_SOD": {"mean": 100, "std_dev": 20},                # SOD in U/mL
    "BIO_GPX": {"mean": 50, "std_dev": 10},                 # GPx in U/gHb
    "BIO_ZN": {"mean": 18, "std_dev": 2.5},                 # Zn in umol/L
    "BIO_CU": {"mean": 20, "std_dev": 3},                   # Cu in umol/L
    "BIO_SE": {"mean": 110, "std_dev": 15},                 # Se in ug/L
    "BIO_HCY": {"mean": 10, "std_dev": 2},                  # Homocystein in umol/L
    "BIO_TAC": {"mean": 1.0, "std_dev": 0.2},               # Total Antioxidant Capacity in mmol/L

    # Neurotransmitters
    "BIO_DOP": {"mean": 1.0, "std_dev": 0.3},               # Dopamine in nmol/L
    "BIO_3_4DOPAC": {"mean": 1.2, "std_dev": 0.4},          # 3,4-DOPAC in nmol/L
    "BIO_HVA": {"mean": 1.0, "std_dev": 0.3},               # HVA in nmol/L
    "BIO_MHPG": {"mean": 1.5, "std_dev": 0.5},              # MHPG in nmol/L
    "BIO_VMA": {"mean": 5.0, "std_dev": 1.5},               # VMA in nmol/L
    "BIO_SER": {"mean": 200, "std_dev": 50},                # Serotonin in nmol/L
    "BIO_5_HIAA": {"mean": 3.0, "std_dev": 1.0},            # 5-HIAA in nmol/L
    "BIO_ADR": {"mean": 0.5, "std_dev": 0.2},               # Adrenaline in nmol/L
    "BIO_NADR": {"mean": 2.0, "std_dev": 0.5},              # Noradrenaline in nmol/L

    # Inflammatory & Protein Workup
    "BIO_TP": {"mean": 70, "std_dev": 5},                 # Total proteins in g/L
    "BIO_A1G": {"mean": 1.5, "std_dev": 0.3},             # Alpha-1 globulins in g/L
    "BIO_A2G": {"mean": 2.0, "std_dev": 0.5},             # Alpha-2 globulins in g/L
    "BIO_BG": {"mean": 2.5, "std_dev": 0.4},              # Beta globulins in g/L
    "BIO_GG": {"mean": 1.0, "std_dev": 0.3},              # Gamma globulins in g/L
    "BIO_ALB": {"mean": 42, "std_dev": 3},                # Albumin in g/L
    "BIO_CRP": {"mean": 2.0, "std_dev": 1.0},             # CRP in mg/L
    "BIO_SUPAR": {"mean": 4.0, "std_dev": 1.0},           # suPAR in ng/mL
    "BIO_HA": {"mean": 100, "std_dev": 30}                # Hyaluronic acid in ng/mL
}


#########################



fake = Faker()
########## DIM TABLES ##########
### DIM_MEMBERS
def generate_dim_members(n_members=1600, first_registered_date="2024-10-01"):
    """
    Generate a synthetic DIM_MEMBERS table with random:
    - Member ID
    - full name
    - DOB
    - Date registered
    - subscription status
    - sex
    """
    first_registered_date = datetime.strptime(first_registered_date, "%Y-%m-%d").date()
    data = []
    for i in range(n_members):
        member_id = i
        full_name = fake.name()
        date_registered = fake.date_between(start_date=first_registered_date, end_date="today")
        date_of_birth = fake.date_between(start_date="-60y", end_date="-20y")
        is_active = random.choice([0, 1])
        sex = random.choice([0,1])
        data.append((member_id, full_name, date_registered, is_active, sex, date_of_birth))

    df_members = pd.DataFrame(data, columns=["Member_ID", "Full_Name", "Date_Registered", "Is_Active", "Sex", "DOB"])
    return df_members

### DIM_CLINICIANS
def generate_dim_clinicians(n_clinicians=20, first_onboarding_date="2023-01-17"):
    """
    Generate a synthetic DIM_MEMBERS table with random:
    - Clinician ID
    - Full Name
    - Zoi_Onboarding_Completion_Date
    """
    first_onboarding_date = datetime.strptime(first_onboarding_date, "%Y-%m-%d").date()
    data = []
    for i in range(n_clinicians):
        clinician_id = i
        name = fake.name()
        onboarding_completion_date = fake.date_between(start_date=first_onboarding_date, end_date="-2m")
        # role = random.choice(["GP", "Cardiologist", "Neurologist", "Dietician", "Physician"])
        data.append((clinician_id, name, onboarding_completion_date))

    df_clinicians = pd.DataFrame(data, columns=["Clinician_ID", "Full_Name", "Is_Zoi_Onboarding_Complete"])

    return df_clinicians

### DIM_BIOMARKERS
def generate_dim_biomarkers():
    """
    Generate a dataframe of biomarkers for DIM_BIOMARKERS table.
    Biomarkers are drawn from Zoi's list of Biological Markers: (oxidative, neurotransmitters, inflammatory, etc.)
    - Biomarker_ID
    - Biomarker_Name
    - Unit_Measurement
    """
    # TODO: create front-end to make it easy for research analysts to add new biomarkers from research papers

    biomarkers_data = [
        # Oxidative
        ("BIO_8OH_DG",  "8OH-DG",        "ug/L"),
        ("BIO_ANTILDL",  "Anti-LDL ox-IgG","mg/dL"),
        ("BIO_COQ10",   "Coenzynme Q10",         "ug/mL"),
        ("BIO_SOD",     "SOD",           "U/mL"),
        ("BIO_GPX",     "GPx",           "U/gHb"),
        ("BIO_ZN",      "Zn",            "umol/L"),
        ("BIO_CU",      "Cu",            "umol/L"),
        ("BIO_SE",      "Se",            "ug/L"),
        ("BIO_HCY",     "Homocystein",  "umol/L"),
        ("BIO_TAC",     "Total Antioxidant Capacity",           "mmol/L"),

        # Neurotransmitters
        ("BIO_DOP",      "Dopamine",                                        "nmol/L"),
        ("BIO_3_4DOPAC", "3,4-Dihydroxyphenylacetic acid (3,4 DOPAC)",       "nmol/L"),
        ("BIO_HVA",      "Homovanillic acid (HVA)",                          "nmol/L"),
        ("BIO_MHPG",     "Methoxy-4-hydroxyphenylglycol (MHPG)",             "nmol/L"),
        ("BIO_VMA",      "Vanillylmandelic acid (VMA)",                      "nmol/L"),
        ("BIO_SER",      "Serotonin",                                        "nmol/L"),
        ("BIO_5_HIAA",   "5-Hydroxyindoleacetic acid (5-HIAA)",              "nmol/L"),
        ("BIO_ADR",      "Adrenaline (Epinephrine)",                         "nmol/L"),
        ("BIO_NADR",     "Noradrenaline (Norepinephrine)",                   "nmol/L"),

        # Inflammatory & Protein workup
        ("BIO_TP",       "Total proteins",                                   "g/L"),
        ("BIO_A1G",      "Alpha-1 globulins",                                "g/L"),
        ("BIO_A2G",      "Alpha-2 globulins",                                "g/L"),
        ("BIO_BG",       "Beta globulins",                                   "g/L"),
        ("BIO_GG",       "Gamma globulins",                                  "g/L"),
        ("BIO_ALB",      "Albumin",                                          "g/L"),
        ("BIO_CRP",      "Ultra-sensitive C-reactive Protein (CRP)",         "mg/L"),
        ("BIO_SUPAR",    "Soluble urokinase plasminogen activator receptor (suPAR)", "ng/mL"),
        ("BIO_HA",       "Hyaluronic acid",                                  "ng/mL")
    ]
    df = pd.DataFrame(
        biomarkers_data,
        columns=["Biomarker_ID","Biomarker_Name","Unit_Measurement"]
    )
    return df

### DIM_DISEASE_PROFILES
def generate_dim_disease_profiles():
    """
    Generate a small list of common disease profiles for DIM_DISEASE_PROFILES table.
    - Disease_Profile_ID
    - Name
    - Last_Reviewed
    """
    # In reality, you’d have a bigger or more clinically rich list
    profiles = [
        {"disease_profile_id":"DIS_001", "name":"Metabolic Syndrome", "last_reviewed":"2024-01-10"},
        {"disease_profile_id":"DIS_002", "name":"Neurodegenerative Risk", "last_reviewed":"2023-11-05"},
        {"disease_profile_id":"DIS_003", "name":"Oxidative Stress Risk", "last_reviewed":"2023-08-21"},
        {"disease_profile_id":"DIS_004", "name":"Cardiovascular Risk", "last_reviewed":"2023-05-15"},
        {"disease_profile_id":"DIS_005", "name":"Parkinson's Disease", "last_reviewed":"2023-03-20"},
        {"disease_profile_id":"DIS_006", "name":"Coronary Artery Disease", "last_reviewed":"2023-02-14"},
        {"disease_profile_id":"DIS_007", "name":"Chronic Liver Disease", "last_reviewed":"2023-01-30"},
        {"disease_profile_id":"DIS_008", "name":"Major Depressive Disorder", "last_reviewed":"2022-12-05"}
    ]
    df = pd.DataFrame(profiles)
    return df.rename(columns={"disease_profile_id":"Disease_Profile_ID", "last_reviewed":"Last_Reviewed", "name":"Disease_Profile_Name"})

### DIM_MEDICAL_DEVICES
def generate_dim_medical_devices():
    """
    Generate a dataframe of medical devices for DIM_MEDICAL_DEVICES table.
    - Medical_Device_ID
    - Name
    - Last_Service_Date
    - Purchased_Date
    """

    devices = [
        {"Medical_Device_ID": "DEV_LC_003", "Name": "LC-MS Biomarker System", "Last_Serviced_Date": "2023-12-01", "Purchased_Date": "2021-09-18"},
        {"Medical_Device_ID": "DEV_ELISA_002", "Name": "Automated ELISA Analyzer", "Last_Serviced_Date": "2023-11-15", "Purchased_Date": "2020-06-12"},
        {"Medical_Device_ID": "DEV_CC_001", "Name": "Automated Clinical Chemistry Analyzer", "Last_Serviced_Date": "2023-10-20", "Purchased_Date": "2019-04-05"},
        {"Medical_Device_ID": "DEV_HPLC_004", "Name": "HPLC with Electrochemical Detection System", "Last_Serviced_Date": "2023-09-30", "Purchased_Date": "2022-01-25"},
        {"Medical_Device_ID": "DEV_ICP_005", "Name": "ICP-MS Trace Element Analyzer", "Last_Serviced_Date": "2023-08-10", "Purchased_Date": "2020-11-02"}
    ]
    return pd.DataFrame(devices)

### DIM_RESEARCH_STUDIES
def generate_dim_research_studies():
    """
    Generate a dataframe of research studies for DIM_RESEARCH_STUDIES table.
    - Research_Study_ID
    - URI
    - Disease_Profile_ID
    """

    # TODO: add more research studies OR just create a feature in "Researcher Portal of streamlit app to easily add research papers and relevant biomarker values"
    research_study_ids = "REAS_0001"
    uri = "https://doi.org/10.3390/biomedicines10071760" # random
    disease_profile_id = "DIS_002" # random, maps to Neurodegenerative Risk

    return pd.DataFrame([{"Research_Study_ID": research_study_ids, "URI": uri, "Disease_Profile_ID": disease_profile_id}])

########## FACT TABLES ##########
def generate_fact_examinations(n_exams=1600):
    """
    Generate a dataframe of examinations for FACT_EXAMINATIONS table.
    - Examination_ID
    - Member_ID
    - Examination_Date
    - Clinician_ID

    Note: n=2000 examinations done assumes 1600 members with a 75% churn rate
    """

    df_members = pd.read_csv("data2/synthetic/dim_members.csv")
    df_clinicians = pd.read_csv("data2/synthetic/dim_clinicians.csv")

    df_members.sort_values(by="Date_Registered", inplace=True)


    examinations = []
    for i in range(n_exams):
        sample_member = df_members.iloc[i]

        # TODO: add a second examination for certain members (when the earliest member registered date is >1 y.o)
        if i > len(df_members):
            # sample random Member_ID provided they are active

            # select random date 1+ year after their last exam date
            pass

        # generate random exam date within a month of Date_Registered
        sample_member_onboarding_date = datetime.strptime(sample_member["Date_Registered"], "%Y-%m-%d").date()
        examination_date = fake.date_between(start_date=sample_member_onboarding_date, end_date="+1m")

        # get sampled member's ID
        member_id =sample_member["Member_ID"]

        # get random clinician from df_clinicians provided they have completed onboarding before the examination date
        random_clinician = df_clinicians.sample(n=1)
        random_clinician_onboarding_date = datetime.strptime(random_clinician.iloc[0]["Is_Zoi_Onboarding_Complete"], "%Y-%m-%d").date()
        while random_clinician_onboarding_date > examination_date:
            random_clinician = df_clinicians.sample(n=1)
            random_clinician_onboarding_date = datetime.strptime(random_clinician.iloc[0]["Is_Zoi_Onboarding_Complete"], "%Y-%m-%d").date()

        examinations.append((member_id, examination_date, random_clinician.iloc[0]["Clinician_ID"]))



    df_examinations = pd.DataFrame(examinations, columns=["Member_ID", "Examination_Date", "Clinician_ID"])
    df_examinations.sort_values(by="Examination_Date", inplace=True)

    examination_ids = [f"EXAM_{i+1:04d}" for i in range(len(df_examinations))]
    df_examinations.insert(0, "Examination_ID", examination_ids)

    return df_examinations

def generate_fact_data_collected():
    """
    Generate a dataframe of data collected for FACT_DATA_COLLECTED table.
    - Data_Collected_ID
    - Examination_ID
    - Biomarker_ID
    - Medical_Device_ID
    - Value
    """

    df_examinations = pd.read_csv("data2/synthetic/fact_examinations.csv")
    df_biomarkers = pd.read_csv("data2/synthetic/dim_biomarkers.csv")

    unique_data_collected_ids = [f"DATA_{i+1:04d}" for i in range(len(df_examinations) * len(df_biomarkers))]

    data_collected = []

    i = 0
    for _, examination in df_examinations.iterrows():
        for _, biomarker in df_biomarkers.iterrows():

            biomarker_id = biomarker["Biomarker_ID"]

            # what medical_device_id is associated with this biomarker?
            # note: normally the medical device making the measurement would be recorded when the biomarker values is recorded
            medical_device_id = BIOMARKER_TO_DEVICE[biomarker_id]

            # what is the value of this biomarker?
            biomarker_value = generate_biomarker_value(biomarker_id)

            data_collected.append((unique_data_collected_ids[i], examination["Examination_ID"], biomarker_id, medical_device_id, biomarker_value))
            i+=1

    return pd.DataFrame(data_collected, columns=["Data_Collected_ID", "Examination_ID", "Biomarker_ID", "Medical_Device_ID", "Value"])

def generate_fact_research_results_values():
    """
    Generate a dataframe of research results for FACT_RESEARCH_RESULTS table.
    - Research_Result_ID
    - Upper_Limit
    - Lower_Limit
    - Population_Size
    - P_Value
    - Confidence_Score
    - Biomarker_ID
    - Research_Study_ID
    """
    # TODO: currently only defined for 1 research study

    df_biomarkers = pd.read_csv("data2/synthetic/dim_biomarkers.csv")

    population_size = random.randint(100, 10000)
    p_value = random.uniform(0, 1)
    confidence_score = random.randint(0, 100) # assuming we have the confidence score is for the entire research study, not for each biomarker
    research_study_id = "REAS_0001"

    research_results = []

    i=1
    for biomarker_id in df_biomarkers["Biomarker_ID"]:
        research_result_id = f"R_RESULTS_{i:04d}"
        upper_limit, lower_limit = generate_biomarker_healthy_range(biomarker_id)

        research_results.append((research_result_id, upper_limit, lower_limit, population_size, p_value, confidence_score, biomarker_id, research_study_id))
        i+=1

    return pd.DataFrame(research_results, columns=["Research_Result_ID", "Upper_Limit", "Lower_Limit", "Population_Size", "P_Value", "Confidence_Score", "Biomarker_ID", "Research_Study_ID"])

#################################
def generate_biomarker_value(biomarker_id):
    """Generates a random value for a given biomarker based on its statistical parameters from `BIOMARKER_PARAMS`."""

    if biomarker_id in BIOMARKER_PARAMS:
        params = BIOMARKER_PARAMS[biomarker_id]
        # assumes normal distribution - in reality, human omics data exhibits kurtosis and skewness
        return np.random.normal(params["mean"], params["std_dev"])
    else:
        raise ValueError(f"Biomarker {biomarker_id} parameters are not defined.")


def generate_biomarker_healthy_range(biomarker_id):
    """Generates a random "healthy range" (ie. upper and lower thresholds) for a given biomarker based on its statistical parameters from `BIOMARKER_PARAMS`."""

    if biomarker_id in BIOMARKER_PARAMS:
        mean = BIOMARKER_PARAMS[biomarker_id]["mean"]
        std_dev = BIOMARKER_PARAMS[biomarker_id]["std_dev"]

        upper_range_a, upper_range_b = mean + 1.5 * std_dev, mean + 2.5 * std_dev
        lower_range_a, lower_range_b = mean - 2.5 * std_dev, mean - 1.5 * std_dev

        upper_limit = random.uniform(upper_range_a, upper_range_b)
        lower_limit = random.uniform(lower_range_a, lower_range_b)

        if upper_limit < lower_limit:
            upper_limit, lower_limit = lower_limit, upper_limit

        return upper_limit, lower_limit

    else:
        raise ValueError(f"Biomarker {biomarker_id} parameters are not defined.")


def generate_synthetic_data(exam: str,
                            n_members= 1600,
                            start_date= "2024-10-01"):

    """
    Create synthethic data for X amount of members

    Arguments:
    - biomarker_type : what kind of data needs to be synthesized? (eg. oxidative, neurological, cardiovascular...)
    # - biomarker_info : what are the key statistical infos of the biomarker data being synthesized? (mean, std, min, max, skewness...)
    - n_members : number of fictitious members to create data for
    - start_date : when is the first date the of the earliest check-up
    """


    # Generate member IDs
    # eg., "Zoi-0001" up to "Zoi-1600"
    member_ids = [f"Zoi-{n+1:04d}" for n in range(n_members)]
    # print(member_ids)

    # Generate random dates representing date of checkup
    # eg. "2024-11-25"
    checkup_dates = [random_date(start_date, datetime.now()) for _ in range(n_members)]
    # print(checkup_dates)

    # Concatenate member IDs and check up date
    member_biomarker_samples = pd.DataFrame({"Check_Up_Date": checkup_dates, "Member_ID": member_ids})

    # if biomarker_info is None:
    #     raise ValueError("Please provide biomarkers_info list with mean, std, min, max, etc.")


    # Generate biomarker data for all members depending on `exam`
    match exam:
        # GOAL RN: Create 1 member sample with synthetic data that has *some* realistic basis
        case "oxidative":
            # TODO: probably should move these schemas directly to the biomarkers.json file
            schema = {
                "8OH-DG": int,
                "SOD": int,
                "GPx": int,
                "CoQ10": int,
                "TAC": int,
                "Zn": int,
                "Cu": int,
                # "Cu:Zn ratio": "ratio",
                "Se": int,
                "Homocysteine": int,
                "Anti-oxLDL IgG": int,
            }

        case "cardiovascular":
            schema = {}

        case "neurological":
            schema = {}


    # Create random values for each biomarker
    for biomarker, value in schema.items():
        biomarker_values = generate_biomarker_random_vals(n_members, exam, biomarker, value)
        member_biomarker_samples =  pd.concat([member_biomarker_samples, biomarker_values], axis=1)


    # # Apply "research-backed" correlations to randomly synthesized data
    # with open("resources/biomarkers.json", 'r') as f:
    #     corr_matrix = json.load(f)[exam]["correlationMatrix"]

    # biomarker_values_corr = correlate_values(corr_matrix, member_biomarker_samples)

    return member_biomarker_samples

def random_date(start_date: datetime, end_date: datetime) -> str:
        """
        Create a random date between two given input dates
        """
        start = datetime.strptime(start_date, '%Y-%m-%d')
        end = end_date
        time_between = end - start
        days_between = time_between.days
        random_days = random.randrange(days_between)
        date = start + pd.Timedelta(days=random_days)
        return f"{date.year}-{date.month}-{date.day}"

def generate_biomarker_random_vals(n_members: int, exam: str, biomarker: str, value: type) -> pd.Series:
    """
    Generate a Series of random values for a given biomarker. Output format depends on type of measured biomarker.
    # TODO: fix docstring
    Arguments:
    - schema : the statistical values that govern the random values' properties
    - biomarker : what biomarker are we generating
    - corr : matrix whose coefficients represent the correlation of the new data with other biomarker data
    """

    member_biomarker_samples = []

    # get pre-researched biomarker data
    with open("resources/biomarkers.json", 'r') as f:
        exam_data = json.load(f)[exam]
        biomarker_data = exam_data[biomarker]
        correlation_matrix = exam_data["correlationMatrix"]


    # NOTE: probably don't need to create a biomarker class if I'm already storing all relevant statistical data for each biomarker in a JSON file
    # biomarker = Biomarker(biomarker_data["biomarker"])

    for _ in range(n_members):

        if value is int:

            raw_value = np.random.normal(loc=biomarker_data["statistics"]["mean"], scale=biomarker_data["statistics"]["std"])
            clamped_value = max(biomarker_data["statistics"]["min"], min(raw_value, biomarker_data["statistics"]["max"]))

            # NOTE: how do I make it correlated to other biomarker values?

            member_biomarker_samples.append(clamped_value)


        elif value is str:
            x = "random_string"
            # not sure what it could be

        elif value == "ratio":
            # get information from biomarkers.json what biomarkers this is a ratio of
            ratio_biomarkers = biomarker_data[biomarker]["ratio_values"]

            # calculate the ratio
            member_biomarker_samples.append(ratio_biomarkers[1] / ratio_biomarkers[0])

            # TODO: substitute for other functions
            # TODO: how to deal with more than 2 biomarkers that are part of the calculation (also, should this be a dbt model since it's techincally data transformation? I should avoid "creating more data" when I can store a model instead of the actual values)

        # TODO: Add some noise + outliers to synthetic data

    return pd.Series(member_biomarker_samples, name=biomarker)

def correlate_values(corr_matrix: np.array, data: pd.DataFrame) -> pd.DataFrame:
    """
    # TODO: Doesn't work
    """
    corr_matrix = np.array(corr_matrix)

    temp_df = data.loc[:, ["Check_Up_Date", "Member_ID"]]
    data.drop(columns=["Check_Up_Date", "Member_ID"], inplace= True)


    # standardize
    scaler = StandardScaler()
    standardized_data = scaler.fit_transform(data)

    # Validate the correlation matrix
    if not np.allclose(corr_matrix, corr_matrix.T):
        raise ValueError("The correlation matrix must be symmetric")
    if not np.all(np.linalg.eigvals(corr_matrix) >= 0):
        raise ValueError("The correlation matrix must be positive semidefinite")

    # transform data to express the same correlation matrix
    cholesky_decomp = np.linalg.cholesky(corr_matrix)

    print(cholesky_decomp.shape)
    print(cholesky_decomp)

    print("======================")
    print(corr_matrix.shape)
    print(corr_matrix)

    correlated_values = standardized_data @ cholesky_decomp.T

    return pd.DataFrame(correlated_values)



# EXAMPLE USAGE:
if __name__ == "__main__":
    # synth_data = generate_synthetic_data(exam="oxidative", n_members=10)
    # print(synth_data)
    # synth_data.to_csv("synthetic_data.csv", index=False)

    # DIM Tables
    df_members = generate_dim_members()
    df_clinicians = generate_dim_clinicians()
    df_biomarkers = generate_dim_biomarkers()
    df_medical_devices = generate_dim_medical_devices()
    df_disease_profiles = generate_dim_disease_profiles()
    df_research_studies = generate_dim_research_studies()

    # FACT Tables
    df_examinations = generate_fact_examinations()
    df_data_collected = generate_fact_data_collected()
    df_research_results = generate_fact_research_results_values()

    current_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(current_dir, "..", "data2", "synthetic")
    absolute_output_dir = os.path.abspath(output_dir)


    # View synthetic data and save to CSV

    ### DIM Tables ###

    # print("df_members")
    # print(df_members)
    # df_members.to_csv(output_dir + "/dim_members.csv", index=False)

    # print("df_clinicians")
    # print(df_clinicians)
    # df_clinicians.to_csv(output_dir + "/dim_clinicians.csv", index=False)

    # print("df_biomarkers")
    # print(df_biomarkers)
    # df_biomarkers.to_csv(output_dir + "/dim_biomarkers.csv", index=False)

    # print("df_medical_devices")
    # print(df_medical_devices)
    # df_medical_devices.to_csv(output_dir + "/dim_medical_devices.csv", index=False)

    # print("df_disease_profiles")
    # print(df_disease_profiles)
    # df_disease_profiles.to_csv(output_dir + "/dim_disease_profiles.csv", index=False)

    # print(df_research_studies)

    ### FACT Tables ###
    # print(df_examinations)
    # df_examinations.to_csv(output_dir + "/fact_examinations.csv", index=False)
    # df_examinations.hist(column="Clinician_ID", bins=20, figsize=(10, 10))
    # plt.show()

    # print(df_data_collected)
    # df_data_collected.to_csv(output_dir + "/fact_data_collected.csv", index=False)
    # df_data_collected.hist(column="Value", by="Biomarker_ID", figsize=(10, 10))
    # plt.show()

    # print(df_research_results)
    # df_research_results.to_csv(output_dir + "/fact_research_results.csv", index=False)
