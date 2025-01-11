import pandas as pd

path = "/Users/seandominique/Projects/Zoi/Data/physionet.org/files/mimiciii-demo/1.4/LABEVENTS.csv"


def show_csv(path):
    df = pd.read_csv(path)

    print("dataframe:")
    print(df.head())
    print("----------")
    print('column names:')
    print(df.columns)

    return

if __name__ == "__main__":
    show_csv(path)
