#include "MPU9250.h"
#include <MPU9250_asukiaaa.h>

#ifdef _ESP32_HAL_I2C_H_
#define SDA_PIN 21
#define SCL_PIN 22
// #define SDA_PIN 18
// #define SCL_PIN 19
#endif

MPU9250 mpu; // You can also use MPU9255 as is
MPU9250_asukiaaa mySensor;
float aX, aY, aZ, aSqrt, gX, gY, gZ, mDirection, mX, mY, mZ;

void setup() {
    Serial.begin(115200);
    Wire.begin();
    delay(2000);

    mpu.setup(0x68);  // change to your own address
    // mpu.setup(0x69);  // change to your own address

    #ifdef _ESP32_HAL_I2C_H_ // For ESP32
    Wire.begin(SDA_PIN, SCL_PIN);
    mySensor.setWire(&Wire);
    #endif

    mySensor.beginAccel();
    mySensor.beginGyro();
    mySensor.beginMag();
}

void loop() {

  uint8_t sensorId;
  int result;

  result = mySensor.readId(&sensorId);

    // PRINT POS FIRST
    if (mpu.update()) {
      
        // Serial.println(
        //   "Pos: "
        // );
        Serial.print(mpu.getYaw()); Serial.print(",");
        Serial.print(mpu.getPitch()); Serial.print(",");
        Serial.print(mpu.getRoll()); Serial.print(",");
    }


  // PRINT VEL
  result = mySensor.gyroUpdate();
  if (result == 0) {
    gX = mySensor.gyroX();
    gY = mySensor.gyroY();
    gZ = mySensor.gyroZ();

    // Serial.println(
    //   "Vel: "
    // );
    Serial.print(gX); Serial.print(",");
        Serial.print(gY); Serial.print(",");
        Serial.print(gZ);  Serial.print(",");
    // Serial.println("gyroX: " + String(gX));
    // Serial.println("gyroY: " + String(gY));
    // Serial.println("gyroZ: " + String(gZ));
  } else {
    // Serial.println("Cannot read gyro values " + String(result));
  }

  // PRINT ACCEL
  result = mySensor.accelUpdate();
  if (result == 0) {
    aX = mySensor.accelX();
    aY = mySensor.accelY();
    aZ = mySensor.accelZ();
    aSqrt = mySensor.accelSqrt();
    // Serial.println("accelX: " + String(aX));
    // Serial.println("accelY: " + String(aY));
    // Serial.println("accelZ: " + String(aZ));
    // Serial.println("accelSqrt: " + String(aSqrt));

    // Serial.println(
    //   "Acc: "
    // );
    Serial.print(aX); Serial.print(",");
        Serial.print(aY); Serial.print(",");
        Serial.println(aZ); //Serial.print(", ");
  } else {
    // Serial.println("Cannod read accel values " + String(result));
  }

  delay(10);
}
