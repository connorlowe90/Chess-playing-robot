#include "motor.h"
#include <Arduino.h>    // Only for serial debug messages

// Current position of the toolhead
float currentX = 0.0;
float currentY = 0.0;

// Moves the X and Y axes in sync so the toolhead moves in a straight line. Moves relative to current position
void moveXYRelative(float distanceX, float distanceY, float speed, float accel){
  Serial.print("Relative move: ");
  Serial.print(distanceX);
  Serial.print(", ");
  Serial.println(distanceY);
  int accelSteps = ceil(speed/accel);

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
  float speedX = sin(angle) * speed;
  float speedY = cos(angle) * speed;

  // Calculate the steps needed to travel the proper distance
  // This needs to be doubled because each loop will toggle the state of the step pin, instead of a full On-Off cycle
  long stepsX = XYstepsPerMM * abs(distanceX) * 2;
  long stepsY = XYstepsPerMM * abs(distanceY) * 2;

  /* Acceleration values. The speed will ramp up over the course of accelSteps cycles to 
  it's full speed and then ramp back down over the same amount of cycles to stop*/
  float speedStepX = speedX / (2*accelSteps);
  float speedStepY = speedY / (2*accelSteps);

  // Set the directions of the XY motors
  setDirection(distanceX, distanceY);

  // Timers for each axis, show how many microseconds since the last pulse to that axis
  unsigned long timerX = 0;
  unsigned long timerY = 0;

  // The current speed of each axis, from which the pulse period is calculated. This will be ramped up and down for acceleration.
  float currentSpeedX = speedStepX;
  float currentSpeedY = speedStepY;

  // The current pulse period for each axis.
  long currentPulseX = 1000000/(speedStepX*XYstepsPerMM);
  long currentPulseY = 1000000/(speedStepY*XYstepsPerMM);

  // The minimum pulse period (max speed) that each axis will hit
  long minPulseX = 1000000/(speedX*XYstepsPerMM);
  long minPulseY = 1000000/(speedY*XYstepsPerMM);

  // Calculate the minimum delay time needed to hit both timer values
  unsigned long gcd = gcd_recurse(minPulseX,minPulseY);
  
  // Bottom out the delay value so the board can still delay accurately
  unsigned long timeStep = max(gcd,10);

  // Amount of steps for each axis left in the current travel
  long stepsLeftX = stepsX;
  long stepsLeftY = stepsY;

  // Current state of the step pins of each axis, will be toggled for motor movement
  bool stepStateX = false;
  bool stepStateY = false;

//  Serial.print("Initial delay is ");
//  Serial.print(currentPulseX);
//  Serial.print(" us, ");
//  Serial.print(currentPulseY);
//  Serial.println(" us");
//  
//  Serial.print("Min delay is ");
//  Serial.print(minPulseX);
//  Serial.print(" us, ");
//  Serial.print(minPulseY);
//  Serial.println(" us");
//  
//  Serial.print("GCD is ");
//  Serial.print(timeStep);
//  Serial.println(" us");
  
  while (stepsLeftX > 0 || stepsLeftY > 0){
    // The arduino cannot delay accurately for less than 3us.
    delayMicro(timeStep);   
    timerX += timeStep;
    timerY += timeStep;
//    Serial.print(stepsLeftX);
//    Serial.print(", ");
//    Serial.println(stepsLeftY);

    // If the X motor still needs to move and it has been the correct time since the last pulse
    if(stepsLeftX > 0 && timerX >= currentPulseX){
      // Reset the timer
      timerX = 0;
      // If nearing the end of the travel, decelerate.
      if(stepsLeftX <= accelSteps * 2){
        currentSpeedX -= speedStepX;
        currentPulseX = 1000000/(currentSpeedX*XYstepsPerMM);
      //If still in the start of the travel, accelerate.
      } else if(stepsX - stepsLeftX < accelSteps * 2){
        currentSpeedX += speedStepX;
        currentPulseX = 1000000/(currentSpeedX*XYstepsPerMM);
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
      } else if(stepsY - stepsLeftY < accelSteps * 2){
        currentSpeedY += speedStepY;
        currentPulseY = 1000000/(currentSpeedY*XYstepsPerMM);
      }
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
  Serial.print("Moving to ");
  Serial.print(x);
  Serial.print(", ");
  Serial.println(y);
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
