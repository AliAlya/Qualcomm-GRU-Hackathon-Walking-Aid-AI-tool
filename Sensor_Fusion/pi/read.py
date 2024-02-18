import serial
import csv
from datetime import datetime
from time import time

# Open serial ports
ser1 = serial.Serial('COM4', 9600)  # Adjust 'COM4' to your device's serial port
ser2 = serial.Serial('COM3', 115200)  # Adjust 'COM3' to your device's serial port

# Open or create a CSV file
with open('obs_' + datetime.now().strftime("%d_%H_%M_%S") + '.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    start = time()
    while True:
        # data = [time() - start]  # Initialize data list with elapsed time
        if ser1.in_waiting > 0 and ser2.in_waiting > 0: # both buffers have data
            line1 = ser1.readline().decode('utf-8').rstrip()  # Read a line from COM4
            data = [time() - start] + line1.split(',') # Prepend timestamp

            line2 = ser2.readline().decode('utf-8').rstrip()  # Read a line from COM3
            data += line2.split(',')  # Append data from COM3

            writer.writerow(data)  # Write combined data to CSV

