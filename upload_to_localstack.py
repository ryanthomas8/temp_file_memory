import boto3
import os
import time

# Set dummy AWS credentials for LocalStack
os.environ["AWS_ACCESS_KEY_ID"] = "test"
os.environ["AWS_SECRET_ACCESS_KEY"] = "test"

# LocalStack S3 Configuration
ENDPOINT_URL = "http://localhost:4566"
BUCKET_NAME = "test-bucket"
FOLDER_PATH = "stress_test_files"

# Initialize LocalStack S3 client
s3 = boto3.client("s3", endpoint_url=ENDPOINT_URL)

def create_bucket(bucket_name):
    """Create an S3 bucket in LocalStack."""
    try:
        s3.create_bucket(Bucket=bucket_name)
        print(f"Bucket '{bucket_name}' created.")
    except s3.exceptions.BucketAlreadyOwnedByYou:
        print(f"Bucket '{bucket_name}' already exists.")

def upload_all_txt_files(bucket_name, folder_path):
    """Upload all .txt files in the folder to LocalStack S3."""
    for filename in os.listdir(folder_path):
        if filename.endswith(".txt"):
            file_path = os.path.join(folder_path, filename)
            with open(file_path, "rb") as file_data:
                s3.put_object(Bucket=bucket_name, Key=filename, Body=file_data)
            print(f"Uploaded: {filename}")

if __name__ == "__main__":
    try:
        create_bucket(BUCKET_NAME)
        time.sleep(1)  # Ensure bucket creation propagates
        upload_all_txt_files(BUCKET_NAME, FOLDER_PATH)
    except Exception as e:
        print(f"Error: {e}")
