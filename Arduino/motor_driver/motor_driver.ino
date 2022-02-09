#include "motor.h"
void setup() {
  // put your setup code here, to run once:
  initPins();
  Serial.println("Starting move...");
  moveXYRelative(20,20,60,20);
  Serial.println("Done");
}

void loop() {
  // put your main code here, to run repeatedly:
  // moveAxisRelative(0,dir,10,70);
//  if(Serial.available() > 0){
//    while(Serial.available() > 0){
//      delay(1);
//     Serial.print(Serial.read());
//    }
//    Serial.println();
//    Serial.println("Moving...");
//    moveXYRelative(10,10,70,50);
//  }
}
