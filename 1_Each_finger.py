import serial
import time
import pandas as pd
from datetime import datetime

# Open serial connection
ser = serial.Serial('COM3', 9600)  # Adjust as per your COM port and baud rate
time.sleep(2)  # Wait for the connection to establish

def collect_data_for_finger(finger_index, duration):
    print(f"Move finger {finger_index + 1}.")
    start_time = time.time()
    sensor_data = []
    timestamps = []
    
    while time.time() - start_time < duration:
        if ser.in_waiting:
            data = ser.readline().decode().strip()
            sensor_values = data.split(',')  # Assuming comma-separated values
            if len(sensor_values) > finger_index:  # Check if the expected sensor data is present
                sensor_data.append(sensor_values[finger_index])  # Collect specific sensor data
                timestamps.append(datetime.now())  # Capture the current time

    return timestamps, sensor_data

data_collection = pd.DataFrame()

# Initial 2 seconds delay
print("Get ready!")
time.sleep(2)

# Collect data for each finger
for i in range(5):  # Assuming five fingers
    timestamps, data = collect_data_for_finger(i, 8)  # Collect for 8 seconds
    if timestamps:  # Check if data was collected
        data_collection[f'Time_Flex{i+1}'] = pd.Series(timestamps)
        data_collection[f'Flex{i+1}'] = pd.Series(data)
        print("Relax.")
        time.sleep(2)  # 2 seconds delay before the next instruction

# Save data to CSV
data_collection.to_csv('Test1_report_movements_with_timestamps.csv', index=False)
print("Data collection complete and saved to 'Test1_movements_with_timestamps.csv'.")
