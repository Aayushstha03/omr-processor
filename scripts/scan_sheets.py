import os
import csv
import random
from datetime import datetime
from omr_processor import getSheetData


SESSION="er_posttest_lab"




# Simulating a folder and filenames (sorted by time)
image_folder = '../sheets_images/'+ SESSION+"_renamed"


image_files = [f for f in os.listdir(image_folder) if os.path.isfile(os.path.join(image_folder, f))]

print(image_files)
# Open a CSV file to write the data
with open(f'../sheets_data/{SESSION}.csv', 'w', newline='') as csvfile:
    csv_writer = csv.writer(csvfile)
    csv_writer.writerow(['roll_no', 'set', 'q1', 'q2', 'q3', 'q4','q5'])

    # Process each image file
    for image_file in image_files:
        image_path = os.path.join(image_folder, image_file)
        
        # Get sheet data from image
        sheet_data = getSheetData(image_path)
        
        # Get set number and answers
        set_number = sheet_data[0]
        answers = sheet_data[1:6]  # Answers for QN1, QN2, QN3, QN4
        
      
        # Convert numbers to answer labels (1 = a, 2 = b, etc.)
        answer_labels = ['a', 'b', 'c', 'd']
        answer_text = [answer_labels[ans] if ans != -1 else 'z' for ans in answers]
        
        # Write row in CSV file
        csv_writer.writerow([image_file[:-4],str(set_number)] + answer_text)
        print("Completed "+image_file)

print("CSV file 'output.csv' generated.")
