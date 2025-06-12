import boto3
import io
import os
import subprocess
import time
import psutil

# Dummy AWS creds for LocalStack
os.environ["AWS_ACCESS_KEY_ID"] = "test"
os.environ["AWS_SECRET_ACCESS_KEY"] = "test"

# S3 and LocalStack config
ENDPOINT_URL = "http://localhost:4566"
BUCKET_NAME = "test-bucket"
TEMP_DIRS = ["/dev/shm", "/tmp"]
BINARY = "wc"  # Replace if needed

def list_objects(bucket):
    s3 = boto3.client("s3", endpoint_url=ENDPOINT_URL)
    response = s3.list_objects_v2(Bucket=bucket)
    return [obj["Key"] for obj in response.get("Contents", [])]

def load_from_s3(bucket, key):
    s3 = boto3.client("s3", endpoint_url=ENDPOINT_URL)
    stream = io.BytesIO()
    s3.download_fileobj(bucket, key, stream)
    stream.seek(0)
    return stream

def write_file(stream, path):
    with open(path, "wb") as f:
        f.write(stream.read())
    return path

def execute(binary, path):
    subprocess.run([binary, path], stdout=subprocess.DEVNULL)

def run_test(temp_path):
    print(f"\n📂 Testing with: {temp_path}")
    object_keys = list_objects(BUCKET_NAME)

    start = time.time()

    for key in object_keys:
        print(f"→ Processing {key}")
        local_path = os.path.join(temp_path, key)

        stream = load_from_s3(BUCKET_NAME, key)
        write_file(stream, local_path)

        execute(BINARY, local_path)
        os.remove(local_path)

    duration = time.time() - start
    print(f"✅ Completed in {duration:.2f} sec")
    return duration

def show_resource_usage():
    print("\n🧠 System resource snapshot:")
    print(f"Memory usage: {psutil.virtual_memory().percent}%")
    print(f"Disk I/O: {psutil.disk_io_counters().write_bytes / (1024**2):.2f} MB written")
    print(f"CPU usage: {psutil.cpu_percent(interval=1)}%")

if __name__ == "__main__":
    results = {}
    for path in TEMP_DIRS:
        if os.path.exists(path):
            try:
                elapsed = run_test(path)
                results[path] = elapsed
            except Exception as e:
                print(f"⚠️ Error with {path}: {e}")
        else:
            print(f"❌ Skipping unavailable path: {path}")

    show_resource_usage()

    print("\n📊 Performance Comparison:")
    for path, dur in results.items():
        print(f"{path}: {dur:.2f} sec")

    if len(results) == 2:
        delta = results[TEMP_DIRS[1]] - results[TEMP_DIRS[0]]
        winner = TEMP_DIRS[0] if delta > 0 else TEMP_DIRS[1]
        print(f"\n🥇 Faster: {winner} by {abs(delta):.2f} sec")
