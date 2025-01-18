import pandas as pd

def classify_finger(movement, reference_value):
    abs_difference = abs(movement - reference_value)
    if abs_difference < 50:
        return 'Severe Impairment'
    elif 50 <= abs_difference < 100:
        return 'Mild Impairment'
    else:
        return 'Normal'

def classify_finger_movements(data):
    reference_row = data.iloc[0]  # Use the first row as reference
    classifications = {}
    for sensor in data.columns:
        if sensor.startswith('Flex'):  # Check if the column starts with 'Flex'
            reference_value = reference_row[sensor]
            data[f'Classification_{sensor}'] = data[sensor].apply(classify_finger, args=(reference_value,))
            classifications[sensor] = data[f'Classification_{sensor}'].mode()[0]
    return classifications

def load_and_classify_data(input_file):
    data = pd.read_csv(input_file)
    classifications = classify_finger_movements(data)
    
    # Save data with labels to a new CSV file
    output_file = input_file.replace('.csv', '_classified.csv')
    data.to_csv(output_file, index=False)
    
    return classifications

# Example usage
input_file = 'Test1_report_processed_data_timestamps.csv'
classifications = load_and_classify_data(input_file)
print("Most frequent classifications for each sensor:")
for sensor, classification in classifications.items():
    if sensor.startswith('Flex'):  # Check if the column starts with 'Flex'
        print(f"{sensor}: {classification}")
