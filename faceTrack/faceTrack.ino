
#include <Servo.h>

  const int potPin = 0;
  const int pitchPin = 5;
  const int yawPin = 3;
  const int servoPause = 100;
  Servo pitchServo , yawServo;
  
  
void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  Serial.println("ready");
  pitchServo.attach(pitchPin);
  yawServo.attach(yawPin);
  
}
long ser;
int pitch = 90;
int yaw = 90;
long y;
long x;

void loop() {
  // put your main code here, to run repeatedly:
  if (Serial.available() > 0){
    ser = Serial.read(); //read serial
    
    if (ser == 121){ //if y
     y = Serial.parseInt();
     pitch = pitch + y;
     pitchServo.write(pitch);

    }

    if (ser == 114){//if right
      yawServo.write(105);
      delay(50);
      yawServo.write(90);
    }

    if (ser == 108){ //if left
      yawServo.write(75);
      delay(50);
      yawServo.write(90);
    }

    Serial.println(ser);
   
  }
  yawServo.write(90);
  delay(servoPause); 

}
