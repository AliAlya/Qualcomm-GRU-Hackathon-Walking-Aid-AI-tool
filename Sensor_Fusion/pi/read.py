import serial
import csv
from datetime import datetime
from time import time

# Open serial port
ser = serial.Serial('COM4', 9600) # Adjust 'COM3' to your Arduino's serial port

# Open or create a CSV file
with open('obs_' + datetime.now().strftime("%d %H_%M_%S") + '.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    start = time()
    while True:
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').rstrip() # Read a line from the serial port
            data = [time() - start] + line.split(',') # Prepend timestamp
            writer.writerow(data) # Write data to CSV
