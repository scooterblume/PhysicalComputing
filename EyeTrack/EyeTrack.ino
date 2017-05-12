
#include <Servo.h>

  const int potPin = 0;
  const int pitchPin = 5;
  const int yawPin = 11;
  const int servoPause = 100;
  const int maxi = 180;
  const int mid = 137;
  const int mini = 95;
  const int led = 7;
  Servo pitchServo;
  Servo yawServo;
  
  
void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  Serial.println("ready");
  yawServo.attach(yawPin);
  pitchServo.attach(pitchPin);
  pitchServo.write(mid);
  yawServo.write(170);
  
}
long ser;
int pitch = mid;

long y;
long x;
int count = 0;

void loop() {
  // put your main code here, to run repeatedly:
  if (Serial.available() > 0){
    count = count +1;
    ser = Serial.read(); //read serial

    if (count == 60){
      count = 0;
      yawServo.write(40);
      delay(250);
      yawServo.write(170);
    }
    
    if (ser == 121){ //if y
      y = Serial.parseInt();
      if (y != mid){ //just wanna light up led
        digitalWrite(led,HIGH);
      }
      else{
        digitalWrite(led,LOW);
      }
      pitch = y;
      pitchServo.write(pitch);
     
    

    }

    Serial.println(ser);
    
  }

  delay(servoPause); 

}
