#include "board.h"
#include <Arduino.h>

// For the Arduino board

const int X_step_pin = 5;
const int X_dir0_pin = 3;
const int X_dir1_pin = 4;

const int Y_step_pin = 5;
const int Y_dir0_pin = 3;
const int Y_dir1_pin = 4;

void initPins(){
  Serial.begin(9600);
  pinMode(X_step_pin,OUTPUT);
  pinMode(X_dir0_pin,OUTPUT);
  pinMode(X_dir1_pin,OUTPUT);
  pinMode(Y_step_pin,OUTPUT);
  pinMode(Y_dir0_pin,OUTPUT);
  pinMode(Y_dir1_pin,OUTPUT);
}

void pinWrite(axis writeAxis, pin writePin, int state){
  switch(writeAxis){
    case X:
      switch(writePin){
        case step:
          digitalWrite(X_step_pin, state);
          break;
        case dir0:
          digitalWrite(X_dir0_pin, state);
          break;
        case dir1:
          digitalWrite(X_dir1_pin, state);
          break;
      }
      break;
      case Y:
      switch(writePin){
        case step:
          digitalWrite(Y_step_pin, state);
          break;
        case dir0:
          digitalWrite(Y_dir0_pin, state);
          break;
        case dir1:
          digitalWrite(Y_dir1_pin, state);
          break;
      }
      break;
  }
}

void delayMicro(int time){
  delayMicroseconds(time);
}
