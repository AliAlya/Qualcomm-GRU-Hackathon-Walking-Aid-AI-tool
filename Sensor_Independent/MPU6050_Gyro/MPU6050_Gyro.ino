#include <Wire.h>

const int MPU = 0x68; // MPU6050 I2C address
float GyroX, GyroY, GyroZ;
float GyroErrorX, GyroErrorY, GyroErrorZ;
float elapsedTime, currentTime, previousTime;
int c = 0;

void setup() {
  Serial.begin(19200);
  Wire.begin();                      // Initialize communication
  Wire.beginTransmission(MPU);       // Start communication with MPU6050
  Wire.write(0x6B);                  // Talk to the register 6B
  Wire.write(0x00);                  // Make reset - place a 0 into the 6B register
  Wire.endTransmission(true);        // End the transmission

  // Call this function if you need to get the IMU error values for your module
  calculate_IMU_error();
  delay(20);
}

void loop() {
  previousTime = currentTime;        // Previous time is stored before the actual time read
  currentTime = millis();            // Current time actual time read
  elapsedTime = (currentTime - previousTime) / 1000.0; // Divide by 1000 to get seconds

  // === Read gyroscope data === //
  Wire.beginTransmission(MPU);
  Wire.write(0x43); // Gyro data first register address 0x43
  Wire.endTransmission(false);
  Wire.requestFrom(MPU, 6, true); // Read 4 registers total, each axis value is stored in 2 registers
  GyroX = (Wire.read() << 8 | Wire.read()) / 131.0; // For a 250deg/s range we have to divide first the raw value by 131.0
  GyroY = (Wire.read() << 8 | Wire.read()) / 131.0;
  GyroZ = (Wire.read() << 8 | Wire.read()) / 131.0;

  // Correct the outputs with the calculated error values
  GyroX = GyroX + GyroErrorX;
  GyroY = GyroY + GyroErrorY;
  GyroZ = GyroZ + GyroErrorZ;

  // Print the angular velocity per second on the serial monitor
  Serial.print("GyroX: ");
  Serial.print(GyroX / elapsedTime);
  Serial.print(" deg/s, ");
  Serial.print("GyroY: ");
  Serial.print(GyroY / elapsedTime);
  Serial.print(" deg/s, ");
  Serial.print("GyroZ: ");
  Serial.print(GyroZ / elapsedTime);
  Serial.println(" deg/s");

  delay(100); // Adjust as needed to control the output rate
}

void calculate_IMU_error() {
  // Omitted for brevity. This function calculates the error values for gyroscopes.
  // You can include it if you need to calibrate your gyroscope.
}
