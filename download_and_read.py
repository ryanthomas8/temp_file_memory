import boto3
import io
import os
import subprocess

# Set dummy AWS credentials for LocalStack
os.environ["AWS_ACCESS_KEY_ID"] = "test"
os.environ["AWS_SECRET_ACCESS_KEY"] = "test"

# AWS S3 Configuration
ENDPOINT_URL = "http://localhost:4566"
BUCKET_NAME = "test-bucket"
OBJECT_KEY = "xyz.txt"

# RAM-backed file path
RAM_FILE_PATH = f"/dev/shm/{OBJECT_KEY}"

def load_from_s3(bucket, key):
    """Download file from S3 directly into an in-memory buffer."""
    s3 = boto3.client("s3", endpoint_url=ENDPOINT_URL)
    
    file_stream = io.BytesIO()
    s3.download_fileobj(bucket, key, file_stream)

    file_stream.seek(0)
    print("File successfully loaded into memory.")
    return file_stream

def write_to_ram(file_stream, file_path):
    """Write the file to RAM-backed storage (/dev/shm)."""
    with open(file_path, "wb") as f:
        f.write(file_stream.read())

    print(f"File written to RAM at {file_path}.")
    return file_path

def execute_binary(binary_path, file_path):
    """Execute the binary with the given file path as an argument."""
    subprocess.run([binary_path, file_path])

if __name__ == "__main__":
    try:
        file_stream = load_from_s3(BUCKET_NAME, OBJECT_KEY)
        file_path = write_to_ram(file_stream, RAM_FILE_PATH)

        binary_path = "cat"  # Update this to your actual binary location
        execute_binary(binary_path, file_path)

        # Clean up after execution
        os.remove(file_path)
    except Exception as e:
        print(f"Error: {e}")
