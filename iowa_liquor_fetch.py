import requests
import json
from dotenv import load_dotenv
import os
from azure.storage.blob import BlobServiceClient
import datetime

# Load .env file
load_dotenv()

# API endpoint and token
api_url = os.getenv('FUNCTION_APP_URL')
app_token = os.getenv('IOWA_API_KEY')

# storage_account_name='azure-storage-blob'
connection_string = os.getenv('AZURE_STORAGE_CONNECTION_STRING')
container_name='dataminingblob'
folder_name = "bronze"


# Get today's date
today = datetime.date(2021, 1, 12) #datetime.date.today()
date_filter = today.strftime("%Y-%m-%d")

# Fetch data for today from the API
headers = {"X-App-Token": app_token}
params = {"$where": f"date = '{date_filter}'", "$limit": 40000}

response = requests.get(api_url, headers=headers, params=params)

print(response.status_code)
print(response.json())

if response.status_code == 200:
    data = response.json()

    # Serialize the JSON data to a string format (in-memory)
    json_data_str = json.dumps(data, indent=2)

    # Define the path in Blob Storage
    blob_path = f"{folder_name}/incremental/daily_sync.json"

    # Upload the JSON data to Azure Blob Storage
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_path)
    blob_client.upload_blob(json_data_str, overwrite=True)
    
    print(f"JSON data for {today} uploaded successfully to: {blob_path}")
else:
    print(f"Failed to fetch data from API. Status code: {response.status_code}")
