import os
import requests
import json
import boto3
from datetime import datetime

# Initialize S3 client and Discord webhook URL
s3 = boto3.client('s3')
bucket_name = 'S3_bucket'  # Replace with your actual S3 bucket name
discord_webhook_url = os.getenv('DISCORD_WEBHOOK_URL')  # Discord webhook URL stored as an environment variable

def generate_presigned_url(file_key):
    """Generate a pre-signed URL for the given S3 file key."""
    return s3.generate_presigned_url(
        'get_object',
        Params={'Bucket': bucket_name, 'Key': file_key},
        ExpiresIn=32400  # URL valid for 9 hours
    )

def get_latest_file_key(sport):
    """Retrieve the latest file key for a given sport."""
    prefix = f'odds_data_{sport}_'
    response = s3.list_objects_v2(Bucket=bucket_name, Prefix=prefix)

    if 'Contents' not in response or len(response['Contents']) == 0:
        print(f"No files found for {sport}")
        return None

    latest_file = sorted(response['Contents'], key=lambda x: x['LastModified'], reverse=True)[0]
    return latest_file['Key']

def post_to_discord_with_latest_odds():
    # Retrieve and post the latest file for each sport individually
    for sport in ['basketball_nba', 'americanfootball_nfl', 'basketball_ncaab', 'americanfootball_ncaaf']:
        prefix = f'odds_data_{sport}_'
        
        try:
            # List objects and sort by LastModified to get the latest file
            response = s3.list_objects_v2(Bucket=bucket_name, Prefix=prefix)
            if 'Contents' in response:
                # Sort files by LastModified in descending order to find the latest file
                latest_file = sorted(response['Contents'], key=lambda x: x['LastModified'], reverse=True)[0]['Key']
                
                # Generate a presigned URL for the latest file
                presigned_url = s3.generate_presigned_url(
                    'get_object',
                    Params={'Bucket': bucket_name, 'Key': latest_file},
                    ExpiresIn=32400  # URL expires in 9 hours
                )
                
                # Compose the message for this sport
                message_content = f"Latest Odds Data for {sport}:\n{presigned_url}"
            else:
                message_content = f"Latest Odds Data for {sport}:\nNo data available."

            # Send each message to Discord individually
            response = requests.post(discord_webhook_url, json={"content": message_content})
            response.raise_for_status()
            print(f"Message for {sport} sent to Discord successfully.")
        
        except Exception as e:
            print(f"Failed to send message to Discord for {sport}: {e}")

def fetch_odds(event, context):
    api_key = os.getenv('API_KEY')  # Use environment variable for the API key
    sports = ['basketball_nba', 'americanfootball_nfl', 'basketball_ncaab', 'americanfootball_ncaaf']
    region = 'us'
    markets = ['h2h', 'spreads', 'totals']  # Markets to include in one file

    for sport in sports:
        combined_data = {}

        for market in markets:
            try:
                url = f'https://api.the-odds-api.com/v4/sports/{sport}/odds'
                params = {
                    'apiKey': api_key,
                    'regions': region,
                    'markets': market,
                    'oddsFormat': 'decimal',
                }

                # Fetch odds data from The Odds API
                response = requests.get(url, params=params)
                response.raise_for_status()  # Raises an error for non-2xx responses
                odds_data = response.json()

                # Store each market type's data under its respective key in combined_data
                combined_data[market] = odds_data

            except requests.exceptions.RequestException as e:
                print(f"Error fetching odds for {sport} ({market}): {e}")
            except Exception as e:
                print(f"Error processing odds data for {sport} ({market}): {e}")

        # Save combined data to S3 with a single file for the sport
        file_name = f'odds_data_{sport}_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
        try:
            s3.put_object(
                Bucket=bucket_name,
                Key=file_name,
                Body=json.dumps(combined_data)
            )
            print(f"Combined odds data for {sport} saved to {file_name} in bucket {bucket_name}")
        except Exception as e:
            print(f"Error saving combined odds data to S3 for {sport}: {e}")

    # Post pre-signed URLs of the latest files to Discord after all odds data has been fetched and saved
    post_to_discord_with_latest_odds()
