import pandas as pd
from scripts.data_gen import generate_synthetic_data
import snowflake.connector
from snowflake.connector.pandas_tools import write_pandas
import os



def upload_dataframe_snowflake(df: pd.DataFrame):
    """
    Upload a pandas DataFrame to Snowflake DB

    Args:
        df (pd.DataFrame): DataFrame to upload
    """

    # try:
    #     conn = snowflake.connector.connect(
    #         user="YOUR_USERNAME",
    #         password="YOUR_PASSWORD",
    #         account="YOUR_ACCOUNT"
    #     )

    #     DKYSASU-LF17384

    #     cur = conn.cursor()

    #     # Upload CSV to Snowflake internal stage
    #     cur.execute("PUT file://path/to/your_file.csv @my_stage")

    #     conn.commit()
    #     cur.close()
    #     conn.close()



    try:
        print(os.getenv("SNOWFLAKE_PASSWORD"))


        conn = snowflake.connector.connect(
            user=os.getenv("SNOWFLAKE_USERNAME"),
            password=os.getenv("SNOWFLAKE_PASSWORD"),
            account=os.getenv("SNOWFLAKE_ACCOUNT"),
            warehouse=os.getenv("SNOWFLAKE_WAREHOUSE"),
            database=os.getenv("SNOWFLAKE_DB"),
            schema=os.getenv("SNOWFLAKE_SCHEMA")
        )

        print("Connected to snowflake")

        cur = conn.cursor()

        cur.execute("create table ZOI_ANALYTICS_DB.DEV_SEAN.SyntheticData_Test2 ('Check_Up_Date' DATE, 'Member_ID' VARCHAR(20), '8OH-DG' NUMBER, 'SOD' NUMBER, 'GPx' INT, 'CoQ10' INT, 'TAC' INT, 'Zn' INT, 'Cu' INT, 'Se' INT, 'Homocysteine' INT, 'Anti-oxLDL IgG' INT)")


        print("Created Table")

        success, nchunks, nrows, _ = write_pandas(
            conn=conn,
            df=df,
            table_name='SyntheticData_Test2',
            database=os.getenv("SNOWFLAKE_DB"),
            schema=os.getenv("SNOWFLAKE_SCHEMA")
        )

        print(f"Successfully uploaded {nrows} rows in {nchunks} chunks to Snowflake.")

    except Exception as e:
        print(f"Error uploading to Snowflake: {str(e)}")
        raise

    finally:
        if 'conn' in locals():
            conn.close()





if __name__ == "__main__":
    member_biomarker_samples = generate_synthetic_data(exam="oxidative", n_members=10)
    # print(member_biomarker_samples.columns)
    upload_dataframe_snowflake(member_biomarker_samples)
