import numpy as np
import pandas as pd
import random
import os
import json
from datetime import datetime
from sklearn.preprocessing import StandardScaler
from faker import Faker
# import Biomarker


########## DIM TABLES ##########
fake = Faker()

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


########## FACT TABLES ##########



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
    print(generate_dim_members())
