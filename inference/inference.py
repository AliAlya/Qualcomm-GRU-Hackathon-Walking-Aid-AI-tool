# import torch
# import torch.nn as nn
# from torch.utils.data import DataLoader, TensorDataset

# import serial
# from datetime import datetime
# import time
# import numpy as np

# class SensorBuffer:
#     def __init__(self, max_size):
#         self.max_size = max_size
#         self.buffer = []
#         self.preds = []

#     def append(self, value, pred):
#         if len(self.buffer) >= self.max_size:
#             self.buffer.pop(0)  # Remove the oldest value
#             self.preds.pop(0)
#         self.buffer.append(value[:])  # Make a copy to ensure the original list is not modified
#         self.preds.append(pred)

#     def get_latest(self):
#         if not self.buffer:
#             raise IndexError("Buffer is empty")
#         return self.buffer[-1]
    
#     def get_avg_pred(self):
#         ls_sum = sum(self.preds)
#         return ls_sum / self.max_size

#     def get_all(self):
#         return self.buffer[:]

# class BinaryClassificationRNN(nn.Module):
#     def __init__(self, input_size, hidden_size, num_layers):
#         super(BinaryClassificationRNN, self).__init__()
#         self.rnn = nn.GRU(input_size, hidden_size, num_layers, batch_first=True)
#         self.fc = nn.Linear(hidden_size, 1)
#         self.sigmoid = nn.Sigmoid()

#     def forward(self, x):
#         # x.shape = (batch_size, sequence_length, input_size)
#         out, (hn, cn) = self.rnn(x)
#         # Select the output of the last time step
#         out = out[:, -1, :]
#         out = self.fc(out)
#         out = self.sigmoid(out)
#         return out
    
# def clean_data(data):
#     if len(data) != 18:
#         return False
    
#     try:
#         float_entries = [float(item) for item in data]
#     except ValueError:
#         return False
    
#     return True
    
# if __name__ == "__main__":
#     # Hyperparameters
#     input_size = 18  # Number of features
#     hidden_size = 128  # Number of features in hidden state
#     num_layers = 2  # Number of stacked LSTM layers

#     # Initialize the model
#     model = BinaryClassificationRNN(input_size, hidden_size, num_layers)
#     model.load_state_dict(torch.load('model_weights.pth'))
#     model.eval()


#     # Open serial ports
#     sensor_buffer = SensorBuffer(max_size=128)
#     ser1 = serial.Serial('COM4', 9600)  # Adjust 'COM4' to your device's serial port
#     ser2 = serial.Serial('COM3', 115200)  # Adjust 'COM3' to your device's serial port

#     freq = 30
#     period = 1 / freq
#     i = 0
#     while True:


#         start = time.time()
#         # data = [time() - start]  # Initialize data list with elapsed time
#         if ser1.in_waiting > 0 and ser2.in_waiting > 0: # both buffers have data
#             line1 = ser1.readline().decode('utf-8').rstrip()  # Read a line from COM4
#             data = line1.split(',') # Prepend timestamp

#             line2 = ser2.readline().decode('utf-8').rstrip()  # Read a line from COM3
#             data += line2.split(',')  # Append data from COM3


#             if clean_data(data):
#                 data = [float(d) for d in data]

                

#             with torch.no_grad():
#                 try:
#                     observation = sensor_buffer.buffer
#                     observation_arr = np.array(observation)
#                     observation_tensor = torch.tensor(observation_arr, dtype=torch.float32).reshape(observation_arr.shape[0], 1, 18)

#                     output = model(observation_tensor)
#                     predictions = output.round().squeeze().numpy()
#                     sensor_buffer.append(data, predictions.mean())
                    

#                 except:
#                     print(data)

#         if i > 29:
#             i = 0
#         else:
#             i += 1
        
#         if i == 29:
#             print("PRED: ", sensor_buffer.get_avg_pred(), end='\n')

#         elapsed = time.time() - start
#         if elapsed < period:
#             time.sleep(period - elapsed)

            

import torch
import torch.nn as nn
import numpy as np
import serial
import time
import requests

offset = 0.0

url = 'https://v6ma9h036i.execute-api.us-east-1.amazonaws.com/default/gait'




class SensorBuffer:
    def __init__(self, max_size):
        self.max_size = max_size
        self.buffer = [[0] * 18]
        self.preds = [0]

    def append(self, value, pred):
        if len(self.buffer) >= self.max_size:
            self.buffer.pop(0)
            self.preds.pop(0)
        self.buffer.append(value)
        self.preds.append(pred)

    def get_latest(self):
        if not self.buffer:
            return None  # Return None instead of raising an error
        return self.buffer[-1]

    def get_avg_pred(self):
        if not self.preds:  # Check if preds is empty
            return 0  # Return 0 or a suitable default value
        return sum(self.preds) / len(self.preds)

    def get_all(self):
        return self.buffer[:]

class BinaryClassificationRNN(nn.Module):
    def __init__(self, input_size, hidden_size, num_layers):
        super().__init__()
        self.rnn = nn.GRU(input_size, hidden_size, num_layers, batch_first=True)
        self.fc = nn.Linear(hidden_size, 1)
        self.sigmoid = nn.Sigmoid()

    def forward(self, x):
        out, _ = self.rnn(x)
        out = self.fc(out[:, -1, :])
        out = self.sigmoid(out)
        return out

def clean_data(data):
    if len(data) != 18:
        return False
    try:
        [float(item) for item in data]
    except ValueError:
        return False
    
    return True

def read_serial_data(serial_device):
    if serial_device.in_waiting > 0:
        line = serial_device.readline().decode('utf-8').rstrip()
        return line.split(',')
    return []

if __name__ == "__main__":
    input_size = 18
    hidden_size = 128
    num_layers = 2

    model = BinaryClassificationRNN(input_size, hidden_size, num_layers)
    model.load_state_dict(torch.load('model_weights.pth'))
    model.eval()

    sensor_buffer = SensorBuffer(max_size=128)
    ser1 = serial.Serial('COM4', 9600)
    ser2 = serial.Serial('COM3', 115200)

    freq = 30
    period = 1 / freq

    post_time = time.time()
    while True:
        start = time.time()
        data1 = read_serial_data(ser1)
        data2 = read_serial_data(ser2)
        data = data1 + data2

        if clean_data(data):            
            data = [float(d) for d in data]
            with torch.no_grad():
                try:
                    if sensor_buffer.buffer:
                        observation_tensor = torch.tensor(sensor_buffer.get_all(), dtype=torch.float32).unsqueeze(1)
                        output = model(observation_tensor)
                        predictions = output.round().squeeze().numpy()
                        sensor_buffer.append(data, predictions.mean())
                except Exception as e:
                    print(f"Error processing data: {e}")

        if len(sensor_buffer.buffer) == sensor_buffer.max_size:
            if time.time() - post_time > 3:
                data = {
                    "id": "1",
                    "value": str(sensor_buffer.get_avg_pred() - offset)
                }

                response = requests.post(url, json=data)

                # Check the response
                print(response.status_code)
                print(response.text)
                response = requests.post(url, json=data)
                post_time = time.time()

            print("PRED:", sensor_buffer.get_avg_pred() - offset)
        else:
            print(len(sensor_buffer.buffer), sensor_buffer.max_size)
        elapsed = time.time() - start
        if elapsed < period:
            time.sleep(period - elapsed)

