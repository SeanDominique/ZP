import pandas as pd
from scripts.data_gen import generate_synthetic_data
import snowflake.connector
from snowflake.connector.pandas_tools import write_pandas
import os
import datetime
from google.cloud import bigquery
import pandas
import pytz
from sqlalchemy import create_engine


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

        # Using SQLAlchemy
        engine = create_engine(
            "snowflake://{user}:{password}@{account}/{database}/{schema}?warehouse={warehouse}".format(
                user="SNOWFLAKE_USER",
                password="SNOWFLAKE_PASSWORD",
                account="SNOWFLAKE_ACCOUNT",
                database="SNOWFLAKE_DB",
                schema="SNOWFLAKE_SCHEMA",
                warehouse="SNOWFLAKE_WAREHOUSE"
            )
        )

        # # Using Python's connector
        # conn = snowflake.connector.connect(
        #     user=os.getenv("SNOWFLAKE_USERNAME"),
        #     password=os.getenv("SNOWFLAKE_PASSWORD"),
        #     account=os.getenv("SNOWFLAKE_ACCOUNT"),
        #     warehouse=os.getenv("SNOWFLAKE_WAREHOUSE"),
        #     database=os.getenv("SNOWFLAKE_DB"),
        #     schema=os.getenv("SNOWFLAKE_SCHEMA"),
        #     verify=False
        # )

        print("Connected to snowflake")

        df.to_sql("SyntheticData_Test2", con=engine, index=False, if_exists="append")

        # cur = conn.cursor()
        # cur.execute("create table ZOI_ANALYTICS_DB.DEV_SEAN.SyntheticData_Test2 ('Check_Up_Date' DATE, 'Member_ID' VARCHAR(20), '8OH-DG' NUMBER, 'SOD' NUMBER, 'GPx' INT, 'CoQ10' INT, 'TAC' INT, 'Zn' INT, 'Cu' INT, 'Se' INT, 'Homocysteine' INT, 'Anti-oxLDL IgG' INT)")

        # print("Created Table")

        # success, nchunks, nrows, _ = write_pandas(
        #     conn=conn,
        #     df=df,
        #     table_name='SyntheticData_Test2',
        #     database=os.getenv("SNOWFLAKE_DB"),
        #     schema=os.getenv("SNOWFLAKE_SCHEMA")
        # )

        print(f"Successfully uploaded n rows in n chunks to Snowflake.")

    except Exception as e:
        print(f"Error uploading to Snowflake: {str(e)}")
        raise

    finally:
        if 'conn' in locals():
            engine.close()

def upload_dataframe_bigquery(df: pd.DataFrame, table_name= "synthetic_data_25_01"):

    print(f"Uploading to Bigquery {table_name}...")

    try:
        client = bigquery.Client()
        table_id = f"zproject-448912.zproject_dbt_demo_db.{table_name}"
        job_config = bigquery.LoadJobConfig(
            schema = [], # used to assist in data type definitions
            # write_disposition="WRITE_TRUNCATE" # if you want dataframe to override existing data in table
        )

        job = client.load_table_from_dataframe(
            df, table_id, job_config=job_config
        )

        job.result()
        print(f"Successfully uploaded to Bigquery {table_name}")

    except Exception as e:
        print(f"Error uploading to Bigquery: {str(e)}")
        raise

    return




if __name__ == "__main__":
    member_biomarker_samples = generate_synthetic_data(exam="oxidative", n_members=10)
    print(member_biomarker_samples)
    print('--------------------------------')
    # print(member_biomarker_samples.columns)
    upload_dataframe_snowflake(member_biomarker_samples)
    # upload_dataframe_bigquery(member_biomarker_samples)
