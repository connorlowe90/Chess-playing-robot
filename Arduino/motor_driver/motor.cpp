#include "motor.h"
#include <stdlib.h>
#include <math.h>
// #include <Arduino.h>    // Only for serial debug messages

// Current position of the toolhead
float currentX = 0.0;
float currentY = 0.0;

// Moves the X and Y axes in sync so the toolhead moves in a straight line. Moves relative to current position
void moveXYRelative(float distanceX, float distanceY, float speed, float accel){

  // Calculate the angle of motion
  float angle;

  // If one of the dimensions is 0, this will lead to a divide by zero case. Instead, just move on the non-zero axis.
  if(distanceX == 0){
    angle = 0;
  } else if (distanceY == 0){
    angle = PI/2;
  } else {
    angle = atan(abs(distanceX / distanceY));
  }

  // Calculate the speed of the x and y axes so the toolhead is moving at the given speed
  float factorX = sin(angle);
  float factorY = cos(angle);
  float speedX = factorX * speed;
  float speedY = factorY * speed;
  float accelX = factorX * accel;
  float accelY = factorY * accel;
  float jerkX = pow(accelX,2) / speedX;
  float jerkY = pow(accelY,2) / speedY;

  // Calculate the steps needed to travel the proper distance
  // This needs to be doubled because each loop will toggle the state of the step pin, instead of a full On-Off cycle
  long stepsX = XYstepsPerMM * abs(distanceX) * 2;
  long stepsY = XYstepsPerMM * abs(distanceY) * 2;

  /* Acceleration values. The speed will ramp up over the course of accelSteps cycles to 
  it's full speed and then ramp back down over the same amount of cycles to stop*/
  float currentAccelX = 0;
  float currentAccelY = 0;
  unsigned long inflectionStepX = pow(accelX,2)/pow(6*jerkX,2);
  unsigned long inflectionStepY = pow(accelY,2)/pow(6*jerkY,2);

  // Set the directions of the XY motors
  setDirection(distanceX, distanceY);

  // Timers for each axis, show how many microseconds since the last pulse to that axis
  unsigned long timerX = 0;
  unsigned long timerY = 0;

  // The current speed of each axis, from which the pulse period is calculated. This will be ramped up and down for acceleration.
  float currentSpeedX = 0;
  float currentSpeedY = 0;

  // The current pulse period for each axis.
  long currentPulseX = 1000000/(jerkX*XYstepsPerMM);
  long currentPulseY = 1000000/(jerkY*XYstepsPerMM);

  // Calculate the minimum delay time needed to hit both timer values
  // unsigned long gcd = gcd_recurse(minPulseX,minPulseY);
  unsigned long timeStep = 10;

  // Amount of steps for each axis left in the current travel
  long stepsLeftX = stepsX;
  long stepsLeftY = stepsY;

  // Current state of the step pins of each axis, will be toggled for motor movement
  bool stepStateX = false;
  bool stepStateY = false;
  
  while (stepsLeftX > 0 || stepsLeftY > 0){
    delayMicro(timeStep);   
    timerX += timeStep;
    timerY += timeStep;

    // If the X motor still needs to move and it has been the correct time since the last pulse
    if(stepsLeftX > 0 && timerX >= currentPulseX){
      // Reset the timer
      timerX = 0;

      // Update acceleration
      if(stepsX - stepsLeftX < inflectionStepX){          // 1st section, ramp up of acceleration
        currentAccelX += jerkX;
      } else if(stepsX - stepsLeftX < inflectionStepX*2){ // 2nd section, ramp down of acceleration
        currentAccelX -= jerkX;
      } else if(stepsLeftX < inflectionStepX){            // 4th section, ramp up of deceleration
        currentAccelX += jerkX;
      } else if(stepsLeftX < inflectionStepX*2){          // 5th section, ramp down of deceleration
        currentAccelX -= jerkX;
      }                                                   // 3rd section, coast (acceleration doesn't change)
      
      // Update speed and pulse period
      currentSpeedX += currentAccelX;
      currentPulseX = 1000000/(currentSpeedX*XYstepsPerMM);

      // Step the motor
      stepStateX = !stepStateX;
      pinWrite(X,step,stepStateX);
      stepsLeftX--;
    }
    
    // If the Y motor still needs to move and it has been the correct time since the last pulse
    if(stepsLeftX > 0 && timerY >= currentPulseY){
      // Reset the timer
      timerY = 0;

      // Update acceleration
      if(stepsY - stepsLeftY < inflectionStepY){          // 1st section, ramp up of acceleration
        currentAccelY += jerkY;
      } else if(stepsY - stepsLeftY < inflectionStepY*2){ // 2nd section, ramp down of acceleration
        currentAccelY -= jerkY;
      } else if(stepsLeftY < inflectionStepY){            // 4th section, ramp up of deceleration
        currentAccelY += jerkY;
      } else if(stepsLeftY < inflectionStepY*2){          // 5th section, ramp down of deceleration
        currentAccelY -= jerkY;
      }                                                   // 3rd section, coast (acceleration doesn't change)
      
      // Update speed and pulse period
      currentSpeedY += currentAccelY;
      currentPulseY = 1000000/(currentSpeedY*XYstepsPerMM);

      // Step the motor
      stepStateY = !stepStateY;
      pinWrite(Y,step,stepStateY);
      stepsLeftY--;
    }
  }
}

// Set the directions of the XY motors
void setDirection(float x, float y){ 
  bool directionX = x >= 0;
  bool directionY = y >= 0;
  pinWrite(X, dir0, directionX);
  pinWrite(X, dir1, !directionX);
  pinWrite(Y, dir0, directionY);
  pinWrite(Y, dir1, !directionY);
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

unsigned long gcd_recurse(unsigned long a, unsigned long b) {
  if (b == 0) return a;
  if (a == 0) return b;
  if (b > a) {
    return gcd_recurse(a, b % a);
  }

  return gcd_recurse(b, a % b);
}
