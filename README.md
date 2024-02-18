## Folder Structure

### Sensor_Fusion
Contains the code that integrates data from multiple sensors on muliple arduinos into the RPi thorugh serial comm.

### Sensor_Independent
Code for independent sensor reading from arduino.

### data
Data gathered from recording optimal and suboptimal gaits used for ML training

### inference
PyTorch scripts to run the trained model on realtime sensor readings, contains the integration of all components on inference side

### model
Model files and notebooks for training the RNN/GRU in PyTorch

### Arduino Libraries
MPU9250-9dof.zip
MPU9250-master.zip
MPU9250_asukiaaa-master.zip
SparkFun_MPU-9250_Breakout_Arduino_Library.zip
