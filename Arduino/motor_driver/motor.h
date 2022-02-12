#ifndef Motor_h
#define Motor_h

#include "board.h"
#include <stdlib.h>
#include <math.h>

// Size of the printer chassis, tool cannot move past these limits
const float MACHINE_BOUND_X = 457.2;
const float MACHINE_BOUND_Y = 584.2;
const float MACHINE_BOUND_Z = 254.0;
const int MICROSTEP_FACTOR = 8;

// Determines the distance the head will move for a rotation of the motor. Likely will need to be calibrated
const int XYstepsPerMM = 6.25 * MICROSTEP_FACTOR;

// Moves the X and Y axes in sync so the toolhead moves in a straight line. Moves relative to current position
void moveXYRelative(float distanceX, float distanceY, float speed, float accel);

// Set the directions of the XY motors
void setDirection(float x, float y);

// Sets the current position as (0,0) in the coordinate system
void setHome();

// Moves the X and Y axes in sync so the toolhead moves in a straight line. Moves to absolute position offset from the home point
void moveXYAbsolute(float x, float y, int speed, int accel);

unsigned long gcd_recurse(unsigned long a, unsigned long b);
#endif
