import csv

# Function to read the first CSV (answers from images)
def read_first_csv(filename):
    with open(filename, mode='r') as file:
        csv_reader = csv.reader(file)
        headers = next(csv_reader)  # Skip header
        data = [row for row in csv_reader]
    return data

# Function to read the second CSV (question data with options and correct answers)
def read_second_csv(filename):
    with open(filename, mode='r') as file:
        csv_reader = csv.reader(file)
        headers = next(csv_reader)  # Skip header
        data = [row for row in csv_reader]
    return data

# Function to match answers from first CSV with the correct ones from the second CSV
def compare_answers(first_csv_data, second_csv_data):
    results = []
    
    for row in first_csv_data:
        file_name = row[0]
        set_number = (row[1])
        user_answers = row[2:6]  # QN1-QN4 answers (a-d)
        
        # Filter data for this set in the second CSV
        set_questions = [q for q in second_csv_data if (q[0]) == set_number]
        print(set_questions)
        # Ensure questions are ordered correctly by QN1-QN4
        
        # Compare user answers with correct answers
        correct_answers = [q[6] for q in set_questions]  # Correct options from second CSV
        correct_flags = [(user_answers[i] == correct_answers[i]) for i in range(4)]
        
        # Add the result for this file
        results.append([file_name, set_number] + correct_flags)
    
    return results

# Write the final results to a new CSV
def write_results_to_csv(results, output_filename):
    with open(output_filename, mode='w', newline='') as file:
        csv_writer = csv.writer(file)
        csv_writer.writerow(['File Name', 'Set', 'QN1', 'QN2', 'QN3', 'QN4'])
        csv_writer.writerows(results)

# File paths
first_csv_file = 'output.csv'  # This file contains the answers from images
second_csv_file = 'questions.csv'  # This file contains the questions with correct answers
output_csv_file = 'comparison_output.csv'  # Final output file with correctness of answers

# Read both CSVs
first_csv_data = read_first_csv(first_csv_file)
second_csv_data = read_second_csv(second_csv_file)

# Compare answers and generate results
comparison_results = compare_answers(first_csv_data, second_csv_data)

# Write results to the output CSV
write_results_to_csv(comparison_results, output_csv_file)

print(f"Comparison results have been written to {output_csv_file}.")
