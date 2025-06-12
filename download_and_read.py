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
RAM_DIR = "/dev/shm"

def list_objects(bucket):
    """List all object keys in the bucket."""
    s3 = boto3.client("s3", endpoint_url=ENDPOINT_URL)
    response = s3.list_objects_v2(Bucket=bucket)
    return [obj["Key"] for obj in response.get("Contents", [])]

def load_from_s3(bucket, key):
    """Download file from S3 directly into an in-memory buffer."""
    s3 = boto3.client("s3", endpoint_url=ENDPOINT_URL)
    file_stream = io.BytesIO()
    s3.download_fileobj(bucket, key, file_stream)
    file_stream.seek(0)
    return file_stream

def write_to_ram(file_stream, file_path):
    """Write the file to RAM-backed storage (/dev/shm)."""
    with open(file_path, "wb") as f:
        f.write(file_stream.read())
    return file_path

def execute_binary(binary_path, file_path):
    """Execute the binary with the given file path as an argument."""
    subprocess.run([binary_path, file_path])

if __name__ == "__main__":
    try:
        object_keys = list_objects(BUCKET_NAME)

        for key in object_keys:
            print(f"Processing: {key}")
            ram_path = os.path.join(RAM_DIR, key)

            file_stream = load_from_s3(BUCKET_NAME, key)
            write_to_ram(file_stream, ram_path)

            binary_path = "wc"  # Replace this with your actual binary
            execute_binary(binary_path, ram_path)

            os.remove(ram_path)
            print(f"✔ Cleaned up {key}")

    except Exception as e:
        print(f"Error: {e}")
