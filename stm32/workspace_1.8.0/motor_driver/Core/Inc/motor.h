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

#define TRAVEL_Z 100	// Height needed to clear the king while holding nothing
#define MOVE_Z 150		// Height needed to clear the king while holding another king

#define MICROSTEP_FACTOR_XY 8		// Microstep setting of the XY motor drivers, 2 = 1/2 stepping, etc.
#define MICROSTEP_FACTOR_Z 1		// Microstep setting of the Z motor drivers, 2 = 1/2 stepping, etc.
#define XY_STEPS_PER_MM 6.25		// Steps needed to travel 1mm in XY using full stepping
#define Z_STEPS_PER_MM 93.75		// Steps needed to travel 1mm in Z using full stepping

/*
 * Standby position of the head, will move to this after a move is complete
 */
#define STANDBY_X MACHINE_BOUND_X
#define STANDBY_Y MACHINE_BOUND_Y
#define STANDBY_Z TRAVEL_Z

/*
 * Speeds and acceleration used for moves
 */
#define XY_SPEED 900
#define Z_SPEED 55
#define XY_ACCELERATION 50000

typedef struct point {
    float x;
    float y;
} point;

typedef struct sizeOfPiece {
    char key;
    double value;
} sizeOfPiece;

// Moves the X and Y axes in sync so the toolhead moves in a straight line. Moves relative to current position
void moveXYRelative(float x, float y);

// Moves the X and Y axes in sync so the toolhead moves in a straight line. Moves to absolute position offset from the home point
void moveXYAbsolute(float x, float y);

// Set the directions of the XY motors
void setDirection(float x, float y);

// Sets the current position as (0,0) in the coordinate system
void setHomeXY();

/*
 * Sets current Z position to be 0
 */
void setHomeZ();

/*
 * Moves the z axis up or down by a given value
 */
void moveZRelative(float z);

/*
 * Moves the z axis to a given height
 */
void moveZAbsolute(float z);

/*
 * Calculates the distance in mm that will be covered in a given time, in seconds
 * Uses speed (mm/s) and acceleration(mm/s^2)
 */
float calcDistance(float time, float speed, float acceleration);

/*
 * Moves a piece between two squares
 * Takes the coordintes of the start and end squares, along with the height of the piece
 */
void movePiece(float startX, float startY, float endX, float endY, float pieceZ);

/*
 * Moves piece using indexes for starting square, ending square, and piece height
 */
void movePieceByIndex(int startIndex, int endIndex, int pieceIndex);

/*
 * Uses index to get the XY coordinates of a square on the board
 */
point getCoordsFromIndex(int index);

/*
 * Moves to the standby position described in motor.h, to be out of the way of the player and the camera
 */
void moveToStandbyPosition();

#endif
