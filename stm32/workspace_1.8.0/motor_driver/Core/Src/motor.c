// Kellen Hartnett
// Adrian Lewis
// Connor Lowe
// Sahibjeet Singh
// Garrett Tashiro
// EE 475, Group 5 Capstone Project

#include "motor.h"

// Current position of the toolhead, assumes it is in standby position at power on
float currentX = STANDBY_X;
float currentY = STANDBY_Y;
float currentZ = TRAVEL_Z;

sizeOfPiece arr[8] = {{'p',43.15}, {'n',52.44}, {'r',43.09}, {'b',61.69}, {'q',73.11}, {'k',88.34}};

point board[64] = {{60.000, 169.000}, {59.571, 209.857}, {59.143, 250.714}, {58.714, 291.571}, {58.286, 332.429}, {57.857, 373.286}, {57.429, 414.143}, {57.000, 455.000},
                   {100.714, 168.571}, {100.265, 209.449}, {99.816, 250.327}, {99.367, 291.204}, {98.918, 332.082}, {98.469, 372.959}, {98.020, 413.837}, {97.571, 454.714},
                   {141.429, 168.143}, {140.959, 209.041}, {140.490, 249.939}, {140.020, 290.837}, {139.551, 331.735}, {139.082, 372.633}, {138.612, 413.531}, {138.143, 454.429},
                   {182.143, 167.714}, {181.653, 208.633}, {181.163, 249.551}, {180.673, 290.469}, {180.184, 331.388}, {179.694, 372.306}, {179.204, 413.224}, {178.714, 454.143},
                   {222.857, 167.286}, {222.347, 208.224}, {221.837, 249.163}, {221.327, 290.102}, {220.816, 331.041}, {220.306, 371.980}, {219.796, 412.918}, {219.286, 453.857},
                   {263.571, 166.857}, {263.041, 207.816}, {262.510, 248.776}, {261.980, 289.735}, {261.449, 330.694}, {260.918, 371.653}, {260.388, 412.612}, {259.857, 453.571},
                   {304.286, 166.429}, {303.735, 207.408}, {303.184, 248.388}, {302.633, 289.367}, {302.082, 330.347}, {301.531, 371.327}, {300.980, 412.306}, {300.429, 453.286},
                   {345.000, 166.000}, {344.429, 207.000}, {343.857, 248.000}, {343.286, 289.000}, {342.714, 330.000}, {342.143, 371.000}, {341.571, 412.000}, {341.000, 453.000}};
                   // top right                                                         // top left


// white capture pieces indices need to be 64-80
point whiteCaptured[17] = {{39, 87}, {79.714, 86.857}, {120.429, 86.714}, {161.143, 85.571}, {201.857, 86.429},
         {242.571, 86.143}, {283.286,86.143}, {324, 86}, {40, 46}, {80.714, 45.929}, {121.429, 45.857},
         {162.143, 45.786}, {202.857, 45.714}, {243.571,45.643}, {284.286, 45.571}, {325, 45.5}, {365, 66}};

// black captured pieces indices need to be 81-97
point blackCaptured[17] = {{35, 534}, {75.429, 534.357}, {115.857, 534.214}, {156.286, 534.071}, {196.714, 533.929},
         {237.143, 533.786}, {277.571, 533.643}, {318, 533.5}, {36, 575.5}, {76.357, 575.357},
         {116.714, 575.214}, {157.071, 575.071}, {197.429, 574.929}, {237.786, 574.786},
         {278.143, 574.643}, {318.5, 574.5}, {358.5, 554}};

// Moves the X and Y axes in sync so the toolhead moves in a straight line. Moves relative to current position
void moveXYRelative(float x, float y){
	float XYmicrostepsPerMM = XY_STEPS_PER_MM * MICROSTEP_FACTOR_XY;

	setDirection(x,y);
	double distanceX = fabs(x);
	double distanceY = fabs(y);

	double angle;

	if(distanceX == 0){
		angle = PI/2;
	} else {
		angle = atan(distanceY/distanceX);
	}


	// X vars
	double speedX = cos(angle) * XY_SPEED;
	double accelTimeX = speedX/XY_ACCELERATION;
	double accelDistanceX = calcDistance(accelTimeX, 0, XY_ACCELERATION);
	double coastDistanceX = distanceX - (accelDistanceX);
	double coastTimeX = coastDistanceX/speedX;

	if(coastTimeX < 0){
		accelTimeX = sqrt(distanceX/XY_ACCELERATION);
		speedX = accelTimeX * XY_ACCELERATION;
		accelDistanceX = calcDistance(accelTimeX, 0, XY_ACCELERATION);
		coastTimeX = 0;
		coastDistanceX = 0;
	}

	unsigned long accelTime_usX = accelTimeX * 1000000.0;
	unsigned long coastTime_usX = coastTimeX * 1000000.0;

	unsigned long stepsX = XYmicrostepsPerMM * distanceX;
	double currentSpeedX = 5;
	unsigned long pulseLengthX = 1000000.0/(currentSpeedX * XYmicrostepsPerMM);

	// Y vars
	double speedY = sin(angle) * XY_SPEED;
	double accelTimeY = speedY/XY_ACCELERATION;
	double accelDistanceY = calcDistance(accelTimeY, 0, XY_ACCELERATION);
	double coastDistanceY = distanceY - (accelDistanceY);
	double coastTimeY = coastDistanceY/speedY;

	if(coastTimeY < 0){
		accelTimeY = sqrt(distanceY/XY_ACCELERATION);
		speedX = accelTimeY * XY_ACCELERATION;
		accelDistanceY = calcDistance(accelTimeY, 0, XY_ACCELERATION);
		coastTimeY = 0;
		coastDistanceY = 0;
	}

	unsigned long accelTime_usY = accelTimeY * 1000000.0;
	unsigned long coastTime_usY = coastTimeY * 1000000.0;

	unsigned long stepsY = XYmicrostepsPerMM * distanceY;
	double currentSpeedY = 5;
	unsigned long pulseLengthY = 1000000.0/(currentSpeedY * XYmicrostepsPerMM);

	// Time
	unsigned long time = 0;
	unsigned long pulseTimerX = 0;
	unsigned long pulseTimerY = 0;
	unsigned long timeStep = 10;

	while(stepsX > 0 || stepsY > 0){
		delayMicro(timeStep);
		time += timeStep;
		pulseTimerX += timeStep;
		pulseTimerY += timeStep;

		// Update X
		if(stepsX > 0 && pulseTimerX >= pulseLengthX){
			pulseTimerX = 0;
			if(time <= accelTime_usX){
				currentSpeedX = XY_ACCELERATION * (time/1000000.0);
			} else if(time > accelTime_usX && time <= (accelTime_usX + coastTime_usX)){
				currentSpeedX = speedX;
			} else {
				currentSpeedX = max((speedX - (XY_ACCELERATION * (time-(accelTime_usX + coastTime_usX))/1000000.0)),speedX);
			}
			pulseLengthX = 1000000/(currentSpeedX * XYmicrostepsPerMM);
			pinWrite(X, step,1);
			delayMicro(10);
			pinWrite(X, step,0);
			time += 10;
			pulseTimerX += 10;
			pulseTimerY += 10;
			stepsX--;
		}

		// Update Y
		if(stepsY > 0 && pulseTimerY >= pulseLengthY){
			pulseTimerY = 0;
			if(time <= accelTime_usY){
				currentSpeedY = XY_ACCELERATION * (time/1000000.0);
			} else if(time > accelTime_usY && time <= (accelTime_usY + coastTime_usY)){
				currentSpeedY = speedY;
			} else {
				currentSpeedY = max((speedY - (XY_ACCELERATION * (time-(accelTime_usY + coastTime_usY))/1000000.0)),speedY);
			}
			pulseLengthY = 1000000.0/(currentSpeedY * XYmicrostepsPerMM);
			pinWrite(Y, step,1);
			delayMicro(10);
			pinWrite(Y, step,0);
			time += 10;
			pulseTimerX += 10;
			pulseTimerY += 10;
			stepsY--;
		}

	}

}

/*
 * Moves the toolhead on XY to coordinates
 */
void moveXYAbsolute(float x, float y){
  moveXYRelative(x-currentX, y-currentY);
  currentX = x;
  currentY = y;
}

 /*
  * Set the directions of the XY motors
  */
void setDirection(float x, float y){
  int directionX = x >= 0;
  int directionY = y >= 0;
  pinWrite(X, dir0, directionX);
  pinWrite(X, dir1, !directionX);
  pinWrite(Y, dir0, directionY);
  pinWrite(Y, dir1, !directionY);
}

/*
 * Sets current XY position to be (0,0)
 * XY home should be the frint right corner
 */
void setHomeXY(){
  currentX = 0.0;
  currentY = 0.0;
}

/*
 * Sets current Z position to be 0
 * Z home should be the top of a pawn
 */
void setHomeZ(){
	currentZ = 0.0;
}

/*
 * Moves the z axis up or down by a given value
 */
void moveZRelative(float z) {
	float ZmicrostepsPerMM = Z_STEPS_PER_MM * MICROSTEP_FACTOR_Z;

	pinWrite(Z,dir0, z < 0);
	unsigned long delay = 1000000/(Z_SPEED * ZmicrostepsPerMM);

	float travelDistance = fabs(z);
	unsigned long steps = ZmicrostepsPerMM * travelDistance;
	for(; steps > 0; steps --){
		pinWrite(Z, step,1);
		delayMicro(10);
		pinWrite(Z, step,0);
		delayMicro(delay);
	}
}

/*
 * Moves the z axis to a given height
 */
void moveZAbsolute(float z){
	moveZRelative(z-currentZ);
	currentZ = z;
}

/*
 * Calculates the distance in mm that will be covered in a given time, in seconds
 * Uses speed (mm/s) and acceleration(mm/s^2)
 */
float calcDistance(float time, float speed, float acceleration){
	return (0.5 * acceleration * pow(time,2)) + (speed * time);
}

/*
 * Moves a piece between two squares
 * Takes the coordintes of the start and end squares, along with the height of the piece
 */
void movePiece(float startX, float startY, float endX, float endY, float pieceZ){

	// Move to the travel height, if not there already
	moveZAbsolute(TRAVEL_Z);

	// Move the the starting square
	moveXYAbsolute(startX,startY);

	// Turn on the magnet
	setMagnet(0);

	// Move down to grab the piece
	moveZAbsolute(pieceZ);


	// Piece is now grabbed

	delayMicro(10000);

	// Move up to be above the other pieces
	moveZAbsolute(MOVE_Z-(arr[5].value - pieceZ - arr[0].value));

	// Move to target square
	moveXYAbsolute(endX,endY);

	// Move down to board
	moveZAbsolute(pieceZ);

	// Release the piece
	setMagnet(1);
	delayMicro(10000);

	// Move back up to travel height
	moveZAbsolute(TRAVEL_Z);
}

/*
 * Moves to the standby position described in motor.h, to be out of the way of the player and the camera
 */
void moveToStandbyPosition(){
	// Move to the travel height, if not there already
	moveZAbsolute(TRAVEL_Z);

	// Move to target square
	moveXYAbsolute(STANDBY_X,STANDBY_Y);
}

/*
 * Moves piece using indexes for starting square, ending square, and piece height
 */
void movePieceByIndex(int startIndex, int endIndex, int pieceIndex){
	point startPoint = getCoordsFromIndex(startIndex);
	point endPoint = getCoordsFromIndex(endIndex);
	float pieceHeight = arr[pieceIndex].value - arr[0].value;
	movePiece(startPoint.x, startPoint.y, endPoint.x, endPoint.y, pieceHeight);

}

/*
 * Uses index to get the XY coordinates of a square on the board
 */
point getCoordsFromIndex(int index){
	if(index > 63 && index < 81){
		return whiteCaptured[index-64];
	} else if (index >= 81){
		return blackCaptured[index-81];
	} else {
		return board[index];
	}
}
