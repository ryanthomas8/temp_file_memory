import os

# Configuration
folder_name = "stress_test_files"
num_files = 1000  # Adjust the number as needed
lines_per_file = 100  # Number of lines in each file

# Make the directory if it doesn't exist
os.makedirs(folder_name, exist_ok=True)

# Generate the .txt files
for i in range(num_files):
    file_path = os.path.join(folder_name, f"file_{i}.txt")
    with open(file_path, "w") as f:
        f.writelines([f"This is file {i}, line {j}\n" for j in range(lines_per_file)])

print(f"✅ Created {num_files} text files in the '{folder_name}' folder.")
