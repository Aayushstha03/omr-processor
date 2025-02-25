import os
import pandas as pd

# Configuration
csv_file = '../student_groups/normalization_posttest_lab.csv'  # Path to the CSV file
image_dir = '../sheets_images/normalization_posttest_lab'   # Path to the directory containing images
output_dir = image_dir+"_renamed"  # Output directory for renamed images
column_name = 'roll_no'     # Column name in the CSV to use for renaming
prefix = 'normalization_posttest_lab_'          # Prefix for renaming files

# Create the output directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)

# Load the CSV file
df = pd.read_csv(csv_file)

# Get the column values as a list
names = df[column_name].dropna().tolist()

# Get the list of image files in the directory
image_files = [f for f in os.listdir(image_dir) if os.path.isfile(os.path.join(image_dir, f))]

# Rename files
for i, (image_file, new_name) in enumerate(zip(image_files, names)):
    # Get the file extension
    ext = os.path.splitext(image_file)[1]
    
    # Create the new file name
    new_filename = f"{prefix}{new_name}{ext}"
    
    # Construct full file paths
    src = os.path.join(image_dir, image_file)
    dst = os.path.join(output_dir, new_filename)
    
    # Rename the file
    os.rename(src, dst)
    print(f"Renamed: {src} -> {dst}")

print("Renaming completed.")
