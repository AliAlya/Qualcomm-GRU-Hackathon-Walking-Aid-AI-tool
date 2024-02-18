#include "Wire.h"       
#include "I2Cdev.h"     
#include "MPU6050.h"    

MPU6050 mpu;
int16_t ax, ay, az;
int16_t gx, gy, gz;

struct MyData {
  byte X;
  byte Y;
  byte Z;
};

MyData data;

void setup()
{
  Serial.begin(9600);
  Wire.begin();
  mpu.initialize();
  //pinMode(LED_BUILTIN, OUTPUT);
}

void loop()
{
  mpu.getMotion6(&ax, &ay, &az, &gx, &gy, &gz);
  data.X = map(ax, -17000, 17000, 0, 255 ); // X axis data
  data.Y = map(ay, -17000, 17000, 0, 255); 
  data.Z = map(az, -17000, 17000, 0, 255);  // Y axis data
  
    // ORIGINAL PRINT
  // Serial.print("Axis X = ");
  // Serial.print(data.X);
  // Serial.print("  ");
  // Serial.print("Axis Y = ");
  // Serial.print(data.Y);
  // Serial.print("  ");
  // Serial.print("Axis Z  = ");
  // Serial.println(data.Z);
  

    // AESTHETIC PRINT

  // Serial.println(
  //   "Acc: "
  // );
  // Serial.print(ax/100); Serial.print(", ");
  // Serial.print(ay/100); Serial.print(", ");
  // Serial.print(az/100); Serial.print(", ");

  // Serial.println(
  //   "Vel: "
  // );
  // Serial.print(gx/100); Serial.print(", ");
  // Serial.print(gy/100); Serial.print(", ");
  // Serial.print(gz/100); Serial.print(", ");

  // Serial.println(
  //   "Pos: "
  // );
  // Serial.print(data.X); Serial.print(", ");
  // Serial.print(data.Y); Serial.print(", ");
  // Serial.println(data.Z); 


    // COMMUNICATION TO PI PRINT

    // POS
      Serial.print(data.X); Serial.print(",");
      Serial.print(data.Y); Serial.print(",");
      Serial.print(data.Z); Serial.print(",");

    // VEL
      Serial.print(gx/100); Serial.print(",");
      Serial.print(gy/100); Serial.print(",");
      Serial.print(gz/100); Serial.print(",");

    // ACC
      Serial.print(ax/100); Serial.print(",");
      Serial.print(ay/100); Serial.print(",");
      Serial.println(az/100); 

  delay(10);
}

