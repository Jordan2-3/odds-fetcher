# odds-fetcher
Lambda function to fetch and send betting odds data to Discord

# Sports Odds Data Automation with AWS and Discord Integration

Overview
This project automates the process of fetching sports betting odds data, storing it in AWS S3, and sending 
notifications with presigned URLs to a Discord channel. It provides real-time updates on sports odds for
basketball (NBA, NCAAB) and football (NFL, NCAAF) directly on a Discord channel. This project leverages AWS Lambda for 
serverless architecture, The Odds API for sports data, and Discord webhooks for notifications.

Features
Automated Data Fetching: Retrieves the latest sports betting odds for multiple sports from The Odds API.
Efficient Data Storage: Saves each sport’s combined odds data in JSON format in AWS S3 with a timestamped file name.
Real-Time Notifications: Sends presigned S3 URLs for each odds file to a specified Discord channel, allowing easy 
  access.
Error Handling & Logging: Provides feedback on API and S3 errors and ensures that notifications adhere to Discord’s 
  message limits.
Serverless Architecture: Uses AWS Lambda for automation, reducing infrastructure maintenance and cost.

Setup Instructions
Prerequisites
1. AWS Account with permissions to create and manage Lambda functions and S3 buckets.
2. Discord Webhook URL: Create a webhook for your Discord channel to receive notifications. 
3. The Odds API Key: Sign up for an API key from The Odds API. Or any other Odds API of choice

AWS Setup
1. Create an S3 Bucket: This will store the JSON files with odds data.
2. Set Up Environment Variables:
  In your Lambda function, set up the following environment variables:
    API_KEY: Your API key from The Odds API.
    DISCORD_WEBHOOK_URL: The webhook URL for your Discord channel.
    BUCKET_NAME: The name of your S3 bucket where the JSON files will be stored.
   
Lambda Function Deployment
1. Upload Code to Lambda:
  Upload fetch_odds.py as the main handler file in your Lambda function.
2. Set the Handler:
  Ensure that the handler is set to fetch_odds.fetch_odds.
3. Add Necessary Permissions:
  Attach policies that allow Lambda to put objects in S3 and execute.

Error Handling
API Errors: Logs and skips the market if The Odds API returns an error.
Discord Character Limit: Ensures that messages are within Discord’s 2000-character limit. If necessary, splits messages by sport to keep within the limit.

python Code Overview
import os
import requests
import json
import boto3
from datetime import datetime

def fetch_odds(event, context):
    # Main function to fetch odds data and send to Discord
    ...

def generate_presigned_url(file_name):
    # Generates a presigned URL for an S3 file
    ...

def post_to_discord_with_latest_odds():
    # Constructs and sends a message with presigned URLs to Discord
    ...



Future plans
