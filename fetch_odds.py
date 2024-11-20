import os
import requests
import json
import boto3
from datetime import datetime

def fetch_odds(event, context):
    api_key = os.getenv('API_KEY')  # Use environment variable for the API key
    sports = ['basketball_nba', 'americanfootball_nfl', 'basketball_ncaab', 'americanfootball_ncaaf']
    region = 'us'
    markets = ['h2h', 'spreads', 'totals']

    # Initialize S3 client
    s3 = boto3.client('s3')
    bucket_name = 'S3-bucket'  # Replace with your actual S3 bucket name

    # Loop through each sport and market type
    for sport in sports:
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

                # Save JSON data to S3 with a unique filename for each sport and market
                file_name = f'odds_data_{sport}_{market}_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
                s3.put_object(
                    Bucket=bucket_name,
                    Key=file_name,
                    Body=json.dumps(odds_data)
                )
                print(f"Odds data for {sport} ({market}) saved to {file_name} in bucket {bucket_name}")

            except requests.exceptions.RequestException as e:
                print(f"Error fetching odds for {sport} ({market}): {e}")
            except Exception as e:
                print(f"Error saving odds data to S3 for {sport} ({market}): {e}")
