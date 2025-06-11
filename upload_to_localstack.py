import boto3
import os
import time

# Set dummy AWS credentials for LocalStack
os.environ["AWS_ACCESS_KEY_ID"] = "test"
os.environ["AWS_SECRET_ACCESS_KEY"] = "test"

# LocalStack S3 Configuration
ENDPOINT_URL = "http://localhost:4566"
BUCKET_NAME = "test-bucket"
FILE_PATH = "xyz.txt"
OBJECT_KEY = "xyz.txt"

# Initialize LocalStack S3 client
s3 = boto3.client("s3", endpoint_url=ENDPOINT_URL)

def create_bucket(bucket_name):
    """Create an S3 bucket in LocalStack."""
    s3.create_bucket(Bucket=bucket_name)
    print(f"Bucket '{bucket_name}' created.")

def upload_file(bucket_name, file_path, object_key):
    """Upload a file to LocalStack S3."""
    with open(file_path, "rb") as file_data:
        s3.put_object(Bucket=bucket_name, Key=object_key, Body=file_data)
    print(f"File '{file_path}' uploaded to '{bucket_name}' as '{object_key}'.")

if __name__ == "__main__":
    try:
        create_bucket(BUCKET_NAME)
        time.sleep(1)  # Ensure bucket creation propagates
        upload_file(BUCKET_NAME, FILE_PATH, OBJECT_KEY)
    except Exception as e:
        print(f"Error: {e}")
