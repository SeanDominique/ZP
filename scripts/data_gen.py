import numpy as np
import pandas as pd
import random
import os
import json
from datetime import datetime
# import Biomarker

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
    member_biomarker_samples = pd.DataFrame({"CheckUp_Date": checkup_dates, "Member_IDs": member_ids})
    print("Member + Dates")
    print(member_biomarker_samples)

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
                "Cu:Zn ratio": "ratio",
                "Se": int,
                "Homocysteine": int,
                "Anti-oxLDL IgG": int,
            }

        case "cardiovascular":
            schema = {}

        case "neurological":
            schema = {}


    for biomarker, value in schema.items():
        biomarker_values = generate_biomarker_random_vals(n_members, exam, biomarker, value)
        member_biomarker_samples =  pd.concat([member_biomarker_samples, biomarker_values], axis=1)


    print(member_biomarker_samples)

    return


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


def generate_biomarker_random_vals(n_members: int, exam: str, biomarker: str, value: str) -> pd.Series:
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
    with open("biomarkers.json", 'r') as f:
        biomarker_data = json.load(f)[exam][biomarker]
        print(biomarker_data)


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




# EXAMPLE USAGE:
if __name__ == "__main__":
    synth_data = generate_synthetic_data(exam="oxidative", n_members=10)
