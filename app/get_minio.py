from minio import Minio
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Access variables
MINIO_DOMAIN = os.getenv("MINIO_DOMAIN")
MINIO_ACCESS_KEY = os.getenv("MINIO_ACCESS_KEY")
MINIO_SECRET_KEY = os.getenv("MINIO_SECRET_KEY")
MINIO_REGION = os.getenv("MINIO_REGION")
MINIO_SECURE = os.getenv("MINIO_SECURE") == "True"

# Create client with access key and secret key with specific region.
client = Minio(
    MINIO_DOMAIN,
    access_key=MINIO_ACCESS_KEY,
    secret_key=MINIO_SECRET_KEY,
    region=MINIO_REGION,
    secure=MINIO_SECURE
)

import os

def download(bucket: str, filename: str):
    # Define the path where you want to save the file
    save_path = f"./data/{filename}"

    # Check if the file already exists
    if os.path.isfile(save_path):
        return {
            "success": False, 
            "message": f"File '{filename}' already exists in '{save_path}'. Download aborted."
        }

    # Create directory if it does not exist
    directory = os.path.dirname(save_path)
    if not os.path.exists(directory):
        os.makedirs(directory)

    try:
        # Assume `client` is already defined and configured to connect to Minio S3 server
        # Get object response from Minio S3 server
        response = client.get_object(bucket, filename)

        # Open a file in binary write mode
        with open(save_path, "wb") as file_data:
            for data in response.stream(32*1024):
                file_data.write(data)
        print(f"File written to {save_path}")

        return {
            "success": True, 
            "message": f"File successfully downloaded and saved to {save_path}", 
            "path": f"{save_path}"
        }
    except Exception as e:
        return {
            "success": False, 
            "message": str(e)
        }
