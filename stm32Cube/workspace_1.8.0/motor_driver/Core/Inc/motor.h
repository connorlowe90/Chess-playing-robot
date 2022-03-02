#ifndef Motor_h
#define Motor_h

#include "board.h"
#include <stdlib.h>
#include <math.h>

#define PI 3.1415926535897932384626433832795
#define max(a,b) \
   ({ __typeof__ (a) _a = (a); \
       __typeof__ (b) _b = (b); \
     _a > _b ? _a : _b; })
#define min(a,b) \
   ({ __typeof__ (a) _a = (a); \
       __typeof__ (b) _b = (b); \
     _a < _b ? _a : _b; })

// Size of the printer chassis, tool cannot move past these limits
#define MACHINE_BOUND_X 456
#define MACHINE_BOUND_Y 583
#define MACHINE_BOUND_Z 252

#define TRAVEL_Z 150

#define MICROSTEP_FACTOR 8
#define MICROSTEP_FACTOR_Z 1
#define XY_STEPS_PER_MM 6.25
#define Z_STEPS_PER_MM 93.75

#define STANDBY_X MACHINE_BOUND_X
#define STANDBY_Y MACHINE_BOUND_Y
#define STANDBY_Z TRAVEL_Z

typedef struct point {
    float x;
    float y;
} point;

typedef struct sizeOfPiece {
    char key;
    double value;
} sizeOfPiece;

// Moves the X and Y axes in sync so the toolhead moves in a straight line. Moves relative to current position
void moveXYRelative(float x, float y, float speed, float acceleration);

// Set the directions of the XY motors
void setDirection(float x, float y);

// Sets the current position as (0,0) in the coordinate system
void setHomeXY();

void setHomeZ();

// Moves the X and Y axes in sync so the toolhead moves in a straight line. Moves to absolute position offset from the home point
void moveXYAbsolute(float x, float y, float speed, float accel);

void moveZAbsolute(float z, float speed, float acceleration);

void moveAxisRelative(axis moveAxis, float distance, float speed, float acceleration);

float calcDistance(float time, float speed, float acceleration);

void BoardCal();

void movePiece(float startX, float startY, float endX, float endY, float pieceZ);

void movePieceByIndex(int startIndex, int endIndex, int pieceIndex);

point getCoordsFromIndex(int index);

void moveToStandbyPosition();

#endif
