import boto3
import json
from datetime import datetime

# Initialize S3 client
s3 = boto3.client('s3')
bucket_name = 'S3_bucket'  # replace with your bucket name

def fetch_latest_odds_data(sport):
    # Assuming files are stored with date prefixes, filter by date
    prefix = f'odds_data_{sport}_'  # Adjust prefix based on your naming convention
    response = s3.list_objects_v2(Bucket=bucket_name, Prefix=prefix)

    if 'Contents' not in response:
        return "No data available for today."

    # Sort files to get the latest
    files = sorted(response['Contents'], key=lambda x: x['LastModified'], reverse=True)
    latest_file = files[0]['Key']

    # Download and read the file content
    obj = s3.get_object(Bucket=bucket_name, Key=latest_file)
    data = json.loads(obj['Body'].read())

    return data  # return as JSON or process further if needed
