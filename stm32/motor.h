#ifndef Motor_h
#define Motor_h

#include "board.h"
#include <stdlib.h>
#include <math.h>

// Size of the printer chassis, tool cannot move past these limits
const float MACHINE_BOUND_X = 457.2;
const float MACHINE_BOUND_Y = 584.2;
const float MACHINE_BOUND_Z = 254.0;

// Determines the distance the head will move for a rotation of the motor. Likely will need to be calibrated
const int XYstepsPerMM = 40;
// Accounts for rounding errors in the acceleration and deceleration. Should be a small value
const float accelDelta = 1.0;

// Moves a single axis relative to it's current position
void moveAxisRelative(axis moveAxis, float distance, int speed);

// Moves the X and Y axes in sync so the toolhead moves in a straight line. Moves relative to current position
void moveXYRelative(float distanceX, float distanceY, float speed, int accelSteps);

// Sets the current position as (0,0) in the coordinate system
void setHome();

// Moves the X and Y axes in sync so the toolhead moves in a straight line. Moves to absolute position offset from the home point
void moveXYAbsolute(float x, float y, int speed, int accel);

#endif