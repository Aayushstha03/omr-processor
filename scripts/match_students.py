import csv


er_data_file="er_data.csv"

def findNormalizationVenue(roll_number: str) -> str:
    try:
        with open(er_data_file, 'r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['roll_no'] == roll_number:
                    return "lab" if row["venue"]=="watrin" else "watrin"
        
        return f"Roll number {roll_number} not found."
    except FileNotFoundError:
        return f"File '{er_data_file}' not found."
    except Exception as e:
        return f"An error occurred: {e}"

# Example usage:
# print(findNormalizationVenue('90123'))



def checkNormalizationRolls(source_file: str = 'normalization_data.csv') -> None:
    incorrect_rolls=[]
    with open(source_file, 'r', newline='', encoding='utf-8') as source:
         

        reader = csv.DictReader(source)
        
        for row in reader:
            roll_number = row['roll_no']
            venueFromER = findNormalizationVenue(roll_number)
            
            if(venueFromER!=row["venue"]):
                print(venueFromER,row["venue"])
                incorrect_rolls.append(row['roll_no'])
            # row['venue'] = venue_info.split(' is ')[1].strip('.')
            

    print(incorrect_rolls)

# Example usage:
checkNormalizationRolls()



def createNormalizationVenue(source_file: str = er_data_file, target_file: str = 'normalization_rolls_venues.csv') -> None:
    with open(source_file, 'r', newline='', encoding='utf-8') as source, \
         open(target_file, 'w', newline='', encoding='utf-8') as target:

        reader = csv.DictReader(source)
        writer = csv.writer(target)
        
        writer.writerow(['roll_no', 'venue'])  # Write header
        
        for row in reader:
            roll_number = row['roll_no']
            venue = findNormalizationVenue(roll_number)
            print(venue)
            
           
            writer.writerow([roll_number, venue])

    print(f"New CSV with roll numbers and venues created: {target_file}")

# Example usage:
# createNormalizationVenue()
