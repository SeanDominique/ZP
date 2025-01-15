import pandas as pd
import json

path = "/Users/seandominique/Projects/Zoi/Data/physionet.org/files/mimiciii-demo/1.4/LABEVENTS.csv"

def show_csv(path):
    df = pd.read_csv(path)

    print("dataframe:")
    print(df.head())
    print("----------")
    print('column names:')
    print(df.columns)

    return 1+1


if __name__ == "__main__":
    # show_csv(path)
    with open("resources/biomarkers.json", 'r') as f:
        biomarker_data = json.load(f)

    df = pd.DataFrame(biomarker_data["oxidative"]["correlationMatrix"])
    print(df)
