import pandas as pd
import boto3
from io import BytesIO
import json

# Initialize S3 client
s3 = boto3.client('s3')

def read_csv_from_s3(bucket_name, file_name):
    # Read CSV data from S3
    response = s3.get_object(Bucket=bucket_name, Key=file_name)
    csv_data = response['Body'].read()

    return csv_data

def csv_to_json(csv_data):
    # Use pandas to read CSV data into a DataFrame
    df = pd.read_csv(BytesIO(csv_data), error_bad_lines=False, header=None, quoting=3, quotechar=',') 

    # Drop columns without names which are the first and second columns
    df = df.iloc[:, 2:]

    # Convert DataFrame to JSON
    json_data = df.to_json(orient='records', lines=True)
    
    return json_data

def lambda_handler(events, context):
    # S3 bucket and file information
    bucket_name = 'lehigh-permit-combined-data-bucket'
    file_name = 'combinedData.csv'  

    # Read CSV data from S3
    csv_data = read_csv_from_s3(bucket_name, file_name)

    # Convert CSV to JSON using pandas, dropping columns without names
    json_data = csv_to_json(csv_data)

    # Save JSON data to S3 and put it in lehigh-permit-combined-data-bucket-json as combinedData.json
    s3.put_object(Body=json_data, Bucket="lehigh-permit-combined-data-bucket-json", Key="combinedData.json")