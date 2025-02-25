import csv



SESSION="er_posttest_lab"
test_type="posttest"

# Function to read the first CSV (answers from images)
def readSheetsData(filename):
    with open(filename, mode='r') as file:
        csv_reader = csv.reader(file)
        headers = next(csv_reader)  # Skip header
        data = [row for row in csv_reader]
    return data

# Function to read the second CSV (question data with options and correct answers)
def readQuestionsData(filename):
    with open(filename, mode='r') as file:
        csv_reader = csv.reader(file)
        headers = next(csv_reader)  # Skip header
        data = [row for row in csv_reader]
    return data


def extractRollNo(text: str):
    before_dot = text.rsplit('.', 1)[0]      # Everything before the last '.'
    after_underscore = before_dot.rsplit('_', 1)[-1]  # Everything after the last '_' in the trimmed text
    return after_underscore


# Function to match answers from first CSV with the correct ones from the second CSV
def compare_answers(sheets_data, questions_data):
    results = []
    
    for row in sheets_data:
        print(row)
        file_name = row[0]
        roll_no=extractRollNo(file_name)
        print(roll_no)
        set_number = (row[1])
        user_answers = row[2:7]  # QN1-QN4 answers (a-d)
   
        # Filter data for this set in the second CSV
        set_questions = [q for q in questions_data if (int(q[0][-1])-1 == int(set_number) and test_type in q[0])]
       
        
        # Compare user answers with correct answers
        correct_answers = [q[6] for q in set_questions]  # Correct options from second CSV
       
        correct_flags = [(user_answers[i] == correct_answers[i]) for i in range(5)]
        
        # Add the result for this file
        results.append([roll_no, set_number] + correct_flags)
    
    return results

# Write the final results to a new CSV
def write_results_to_csv(results, output_filename):
    with open(output_filename, mode='w', newline='') as file:
        csv_writer = csv.writer(file)
        csv_writer.writerow(['roll_no', 'set', 'q1', 'q2', 'q3', 'q4','q5'])
        csv_writer.writerows(results)

# File paths
first_csv_file = f"../sheets_data/{SESSION}.csv"  # This file contains the answers from images
second_csv_file = '../temp_data/questions.csv'  # This file contains the questions with correct answers
output_csv_file = f'{SESSION}.csv'  # Final output file with correctness of answers

# Read both CSVs
sheets_data = readSheetsData(first_csv_file)
questions_data = readQuestionsData(second_csv_file)

# Compare answers and generate results
comparison_results = compare_answers(sheets_data, questions_data)

# Write results to the output CSV
write_results_to_csv(comparison_results, output_csv_file)

print(f"Comparison results have been written to {output_csv_file}.")
