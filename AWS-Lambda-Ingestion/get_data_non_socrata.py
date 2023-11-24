"""This script pulls data directly from a CSV file from API and saves it as a CSV file. """
"""This script is designed for AWS Lambda deployment, not local."""
import logging
import pandas as pd
from sodapy import Socrata
import os
import sys
import boto3
import psutil
from io import BytesIO
    # Dictionary of cities and their corresponding API information
META_CITY = {"new_york":("socrata", "data.cityofnewyork.us", "dm9a-ab7w", "job_start_date", "VMy8JkExlzdzLuhhl0hPPjLOe"),
            "chicago": ("socrata", "data.cityofchicago.org", "ydr8-5enu", "issue_date", "OeO911BbttwbWOl2CkPqg8MJP"),
            "mesa": ("socrata", "data.mesaaz.gov", "2gkz-7z4f", "issued_date", "ibJlwU98NuWQ0xQoN4IA9FvNU"),
            "la": ("socrata", "data.lacity.org", "nbyu-2ha9", "issue_date", "UKh6YfyKpAyOjVFPdmJBTMO6K"),
            "austin": ("socrata", "data.austintexas.gov", "3syk-w9eu", "issue_date", "BYLqtbK6NfyFXdfpPDrVEA2uO"),
            "philly": ("non_socrata", "https://phl.carto.com/api/v2/sql?filename=permits&format=csv&skipfields=cartodb_id,the_geom,the_geom_webmercator&q=SELECT%20*,%20ST_Y(the_geom)%20AS%20lat,%20ST_X(the_geom)%20AS%20lng%20FROM%20permits%20WHERE%20permitissuedate%20%3E=%20%272016-01-01%27", "permitissuedate"),
            "philly_valuation": ("non_socrata", "https://opendata-downloads.s3.amazonaws.com/opa_properties_public.csv", "assessment_date")}

# Number of times the script will try to get data from a Socrata API
SOCRATA_TRIES = 3
# Max number of rows to call for the Socrata API for testing
ROW_LIMIT = 1_000
# Client to connect to s3 bucket
s3 = boto3.client('s3')
# raw_data bucket name
bucket_name = "lehigh-permit-raw-data-bucket"
# logger information
logging.basicConfig(stream=sys.stdout)
logger = logging.getLogger("get_data")
logger.setLevel(logging.INFO)

def upload_df_to_s3(df, bucket_name, s3_file_name):    
    # Convert Dataframe to CSV String
    csv_data = df.to_csv(index=False)
    
    #Upload the CSV string to s3
    s3.put_object(Body = csv_data, Bucket = bucket_name, Key = s3_file_name)
    
def get_data(url, location, date_column) -> None:
    """
    Pulls data from a Non-Socrata source and saves it as a csv file
    :param url: the url of the api
    :param location: the name of the location
    :return: None
    """
    # Use Pandas to read the CSV file from the URL
    # Save the CSV file to the current directory
    df = pd.read_csv(url)
    # Check if the file exists in the S3 bucket "lehigh-permit-raw-data-bucket"
    file_exists = True
    try:
        s3.head_object(Bucket= bucket_name, Key=f"{location}.csv")
    except Exception as e:
        file_exists = False
        logger.info(f"No previous version of {location}.csv found, creating and saving new {location}.csv")
        
    if file_exists:
         # Download the file from S3
        response = s3.get_object(Bucket= bucket_name, Key= f"{location}.csv")
        data = response['Body'].read()
        # Convert the bytes to a pandas DataFrame
        df_original = pd.read_csv(BytesIO(data))
        # sort the df by the permitissuedate column
        df_original = df_original.sort_values(by=date_column, ascending=False)
        most_recent_date = df_original[date_column][0]
        df = df[df[date_column] > most_recent_date]
        df = df.append(df_original)
        logger.info(f"{location}.csv updated with the latest information.")
        
    #upload dataframe to s3 bucket as a csv
    upload_df_to_s3(df, 'lehigh-permit-raw-data-bucket', f'{location}.csv')

def lambda_handler(events, context):
    locations = ["new_york", "chicago", "mesa", "la", "austin", "philly", "philly_valuation"]
    for place in locations:
        meta = META_CITY[place]
        if meta[0] == "non_socrata":
            try:
                get_data(meta[1], place, meta[2])
                logger.info(f"Saved {place}.csv")
            except Exception as e:
                logger.error(e)
    # print memory used
    memory_used = psutil.Process(os.getpid()).memory_info().rss / 1024 ** 2
    print("Memory Used: " + str(memory_used) + " MiB")
    return {
        'statusCode': 200
    }

