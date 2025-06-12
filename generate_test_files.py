import os
import base64

# Configuration for ~1 GB total
folder = "stress_test_files"
text_file_count = 20
base64_file_count = 20
binary_file_count = 20

# Each text file ≈ 15 MB
text_lines_per_file = 15000
line_content = "This is a long line of text to inflate file size significantly. " * 20 + "\n"

# Each binary file = 20 MB
binary_file_size_mb = 20

# Each base64 file starts from ~12 MB raw (~16 MB after encoding)
base64_input_bytes = 12 * 1024 * 1024

# Create output folder
os.makedirs(folder, exist_ok=True)

# Generate text files
for i in range(text_file_count):
    with open(os.path.join(folder, f"text_file_{i}.txt"), "w") as f:
        f.writelines([line_content for _ in range(text_lines_per_file)])

# Generate base64-encoded random files
for i in range(base64_file_count):
    with open(os.path.join(folder, f"base64_file_{i}.txt"), "w") as f:
        rand_bytes = os.urandom(base64_input_bytes)
        f.write(base64.b64encode(rand_bytes).decode())

# Generate binary files
for i in range(binary_file_count):
    with open(os.path.join(folder, f"binary_file_{i}.bin"), "wb") as f:
        f.write(os.urandom(binary_file_size_mb * 1024 * 1024))

print("✅ All ~1 GB of test files created successfully.")
