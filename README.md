# Gait Aid: Proper and Improper Walking Habit Analyzer

## Overview
The **Gait Aid** project is a sensor-based application designed to measure and analyze proper and improper walking habits using real-time sensor data. It utilizes multiple MPU9250 sensors to collect motion data, which is processed through a trained Recurrent Neural Network (RNN) model to classify walking habits as optimal or suboptimal. The project integrates embedded systems, machine learning, cloud APIs, and the Qualcomm HDK8450 hardware for service app execution.

---

## Features
- **Real-Time Sensor Integration**:
  - Multiple MPU9250 sensors connected via Arduino and Raspberry Pi.
  - Serial communication for data transfer.

- **Machine Learning Model**:
  - PyTorch-based RNN/GRU model for binary classification of walking habits.
  - Pre-trained on a dataset of optimal and suboptimal gait recordings.

- **Cloud Integration**:
  - Sends inference results to an AWS Lambda function for further processing.
  - REST API integration for remote data storage and analysis.

- **Service Application**:
  - Runs on the Qualcomm HDK8450 development kit for app execution and data visualization.

- **CSV Logging**:
  - Data logging for sensor values to CSV files for training and validation.

---

## Project Structure
- **`Sensor_Fusion/`**:
  - Code to integrate multiple Arduino sensors with Raspberry Pi via serial communication.

- **`Sensor_Independent/`**:
  - Code for independent sensor readings from Arduino.

- **`data/`**:
  - CSV files containing training data for optimal and suboptimal gaits.

- **`inference/`**:
  - PyTorch scripts for running the trained model on real-time sensor readings.
  - Integration of all components for live inference.

- **`model/`**:
  - Notebooks and scripts for training the RNN/GRU model in PyTorch.
  - Saved model weights (`model_weights.pth`).

- **Arduino Libraries**:
  - `MPU9250-9dof.zip`
  - `MPU9250-master.zip`
  - `MPU9250_asukiaaa-master.zip`
  - `SparkFun_MPU-9250_Breakout_Arduino_Library.zip`

---

## Requirements
- **Hardware**:
  - MPU9250 sensors.
  - Arduino boards.
  - Raspberry Pi for central processing.
  - Qualcomm HDK8450 for running the service app.
  - USB/Serial cables for communication.

- **Software**:
  - Python 3.8+.
  - PyTorch for machine learning.
  - Serial library for data reading.
  - AWS account for API integration.

---

## How It Works
1. **Sensor Data Collection**:
   - MPU9250 sensors collect motion data (acceleration, gyroscope, and magnetometer).
   - Data is transmitted to Raspberry Pi via serial communication.

2. **Preprocessing**:
   - Data is cleaned and formatted into 18 features for model input.

3. **Inference**:
   - A trained RNN model processes the sensor data to predict walking habits.
   - Predictions are averaged in real-time using a sliding buffer.

4. **Cloud Integration**:
   - Results are sent to an AWS Lambda endpoint for logging and further analysis.

5. **Service App**:
   - Runs on the Qualcomm HDK8450, displaying processed data and providing insights.

6. **Visualization**:
   - Gait habits are classified as optimal or suboptimal and visualized for users.

---

## Running the Project
### Hardware Setup
1. Connect MPU9250 sensors to Arduino.
2. Link Arduino boards to Raspberry Pi via USB.
3. Connect the Qualcomm HDK8450 for service app execution.
4. Ensure all devices are powered and connected.

### Software Setup
1. Install dependencies:
   ```bash
   pip install torch numpy serial requests
   ```
2. Train the model (if needed):
   - Use scripts in the `model/` directory.
3. Run inference:
   ```bash
   python inference.py
   ```

### Data Logging
- Use scripts in the `Sensor_Independent/` or `Sensor_Fusion/` directories to collect and log sensor data.

---

## Example Output
- **Prediction**: Proper gait: 0.85 (confidence score).
- **AWS Response**:
  ```json
  {
    "statusCode": 200,
    "body": "Gait data received successfully"
  }
  ```

---

## Future Enhancements
- Improve model accuracy with additional training data.
- Add a mobile app for real-time feedback and visualization.
- Optimize sensor fusion algorithms for better data integration.
