import csv

def process_sensor_data(input_file, output_file):
    with open(input_file, 'r') as input_csv, open(output_file, 'w', newline='') as output_csv:
        reader = csv.reader(input_csv)
        writer = csv.writer(output_csv)
        
        
        header = next(reader)
        sensor_header = [col for col in header if "Flex" in col]
        writer.writerow(sensor_header)
        
        
        prev_values = [None] * len(sensor_header)
        
        for row in reader:
            processed_row = []
            sensor_values = [row[header.index(col)] for col in sensor_header if col in header]  # Extract sensor data only
            
            
            for i, current_value in enumerate(sensor_values):
                current_value = current_value.strip()
                
                
                if not current_value:
                    above_value = prev_values[i] if prev_values[i] is not None else ''
                    current_value = above_value
                
                try:
                    
                    current_value = int(current_value)
                    
                    
                    if prev_values[i] is not None and abs(current_value - int(prev_values[i])) > 2000:
                        current_value = prev_values[i]
                except ValueError:
                    
                    current_value = prev_values[i] if prev_values[i] is not None else ''
                
                processed_row.append(current_value)
                
                prev_values[i] = current_value
            
            
            writer.writerow(processed_row)

# Example usage
input_file = 'Test1_report_movements_with_timestamps.csv'
output_file = 'Test1_report_processed_data_timestamps.csv'
process_sensor_data(input_file, output_file)
