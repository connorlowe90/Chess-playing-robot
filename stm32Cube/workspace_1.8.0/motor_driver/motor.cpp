#include "motor.h"
#include <Arduino.h>    // Only for serial debug messages
// Current position of the toolhead
float currentX = 0.0;
float currentY = 0.0;

// Moves a single axis relative to it's current position
void moveAxisRelative(axis moveAxis, float distance, int speed){
  
  // Calculate the steps needed to make the move, and the pulse period needed to move at the given speed
  int XYsteps = XYstepsPerMM * abs(distance);
  int pulsePeriod = 1000000/(speed*XYstepsPerMM);

  // Set the direction of the motor
  bool direction = (distance >= 0);
  pinWrite(moveAxis, dir0, direction);
  pinWrite(moveAxis, dir1, !direction);

  // Pulse the step pin
  for(int i=0; i<XYsteps; i++){
    pinWrite(moveAxis, step, true);
    delayMicro(pulsePeriod);
    pinWrite(moveAxis, step, false);
    delayMicro(pulsePeriod);
  }
}

// Moves the X and Y axes in sync so the toolhead moves in a straight line. Moves relative to current position
void moveXYRelative(float distanceX, float distanceY, float speed, int accelSteps){

  // If one of the dimensions is 0, this will lead to a divide by zero case. Instead, just move on the non-zero axis.
  if(distanceX == 0){
    moveAxisRelative(Y, distanceY, speed);
  } else if (distanceY == 0){
    moveAxisRelative(X, distanceX, speed);
  }

  // Calculate the speed of the x and y axes so the toolhead is moving at the given speed
  float angle = atan(abs(distanceX / distanceY));
  float speedX = cos(angle) * speed;
  float speedY = sin(angle) * speed;

  // Calculate the steps needed to travel the proper distance
  // This needs to be doubled because each loop will toggle the state of the step pin, instead of a full On-Off cycle
  int stepsX = XYstepsPerMM * abs(distanceX) * 2;
  int stepsY = XYstepsPerMM * abs(distanceY) * 2;

  /* Acceleration values. The speed will ramp up over the course of accelSteps cycles to 
  it's full speed and then ramp back down over the same amount of cycles to stop*/
  float speedStepX = speedX / (2*accelSteps);
  float speedStepY = speedY / (2*accelSteps);

  // Set the directions of the motors
  bool directionX = distanceX >= 0;
  bool directionY = distanceY >= 0;
  pinWrite(X, dir0, directionX);
  pinWrite(X, dir1, !directionX);
  pinWrite(Y, dir0, directionY);
  pinWrite(Y, dir1, !directionY);

  // Pulse loop
  int timerX = 0;
  int timerY = 0;
  float currentSpeedX = speedStepX;
  float currentSpeedY = speedStepY;
  long currentPulseX = 1000000/(speedStepX*XYstepsPerMM);
  long currentPulseY = 1000000/(speedStepY*XYstepsPerMM);
  int stepsLeftX = stepsX;
  int stepsLeftY = stepsY;
  bool stepStateX = false;
  bool stepStateY = false;

  Serial.print("Initial delay is ");
  Serial.print(currentPulseX / 1000);
  Serial.println(" ms");
  
  while (stepsLeftX > 0 && stepsLeftY > 0){
    // The loop time is 10us, since the arduino cannot delay accurately for less than 3us.
    delayMicro(10);
    timerX += 10;
    timerY += 10;

    // If the X motor still needs to move and it has been the correct time since the last pulse
    if(stepsLeftX > 0 && timerX >= currentPulseX){
      
      // Reset the timer
      timerX = 0;

      // If nearing the end of the travel, decelerate.
      if(stepsLeftX <= accelSteps * 2){
        currentSpeedX -= speedStepX;
        currentPulseX = 1000000/(currentSpeedX*XYstepsPerMM);
        Serial.print("Decelerating to ");
        Serial.print(currentSpeedX);
        Serial.println(" mm/s");
        
      //If still in the start of the travel, accelerate.
      } else if(stepsX - stepsLeftX < accelSteps * 2){
        currentSpeedX += speedStepX;
        currentPulseX = 1000000/(currentSpeedX*XYstepsPerMM);
        Serial.print("Accelerating to ");
        Serial.print(currentSpeedX);
        Serial.println(" mm/s");
      }
      stepStateX = !stepStateX;
      pinWrite(X,step,stepStateX);
      stepsLeftX--;
    }
    
    // If the Y motor still needs to move and it has been the correct time since the last pulse
    if(stepsLeftY > 0 && timerY >= currentPulseY){
      
      // Reset the timer
      timerY = 0;

      // If nearing the end of the travel, decelerate.
      if(stepsLeftY <= accelSteps * 2){
        currentSpeedY -= speedStepY;
        currentPulseY = 1000000/(currentSpeedY*XYstepsPerMM);
        
      //If still in the start of the travel, accelerate.
      } else if(stepsY - stepsLeftY < accelDelta * 2){
        currentSpeedY += speedStepY;
        currentPulseY = 1000000/(currentSpeedY*XYstepsPerMM);
      }
      stepStateY = !stepStateY;
      pinWrite(Y,step,stepStateY);
      stepsLeftY--;
    }
  }
}

void setHome(){
  currentX = 0.0;
  currentY = 0.0;
}

void moveXYAbsolute(float x, float y, int speed, int accel){
  moveXYRelative(x-currentX, y-currentY, speed, accel);
  currentX = x;
  currentY = y;
}
