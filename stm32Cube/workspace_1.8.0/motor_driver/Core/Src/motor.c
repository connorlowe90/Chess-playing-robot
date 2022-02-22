#include "motor.h"
//#include <Arduino.h>    // Only for serial debug messages

// Current position of the toolhead
float currentX = 0.0;
float currentY = 0.0;
float currentZ = 0.0;

// Moves the X and Y axes in sync so the toolhead moves in a straight line. Moves relative to current position
void moveXYRelative(float x, float y, float speed, float acceleration){
	float XYmicrostepsPerMM = XY_STEPS_PER_MM * MICROSTEP_FACTOR;

	setDirection(x,y);
	float distanceX = fabs(x);
	float distanceY = fabs(y);

	float angle;

	if(x == 0){
		angle = PI/2;
	} else {
		angle = atan(distanceY/distanceX);
	}


	// X vars
	float speedX = cos(angle) * speed;
	float accelTimeX = speedX/acceleration;
	float accelDistanceX = calcDistance(accelTimeX, 0, acceleration);
	float coastDistanceX = distanceX - (2*accelDistanceX);
	float coastTimeX = coastDistanceX/speedX;

	if(coastTimeX < 0){
		speedX = sqrt(distanceX/acceleration);
		accelTimeX = speedX/acceleration;
		accelDistanceX = calcDistance(accelTimeX, 0, acceleration);
		coastTimeX = 0;
		coastDistanceX = 0;
	}

	unsigned long accelTime_usX = accelTimeX * 1000000;
	unsigned long coastTime_usX = coastTimeX * 1000000;

	unsigned long stepsX = XYmicrostepsPerMM * distanceX;
	float currentSpeedX = 5;
	unsigned long pulseLengthX = 1000000/(currentSpeedX * XYmicrostepsPerMM);

	// Y vars
	float speedY = sin(angle) * speed;
	float accelTimeY = speedY/acceleration;
	float accelDistanceY = calcDistance(accelTimeY, 0, acceleration);
	float coastDistanceY = distanceY - (2*accelDistanceY);
	float coastTimeY = coastDistanceY/speedY;

	if(coastTimeY < 0){
		speedY = sqrt(distanceY/acceleration);
		accelTimeY = speedY/acceleration;
		accelDistanceY = calcDistance(accelTimeY, 0, acceleration);
		coastTimeY = 0;
		coastDistanceY = 0;
	}

	unsigned long accelTime_usY = accelTimeY * 1000000;
	unsigned long coastTime_usY = coastTimeY * 1000000;

	unsigned long stepsY = XYmicrostepsPerMM * distanceY;
	float currentSpeedY = 5;
	unsigned long pulseLengthY = 1000000/(currentSpeedY * XYmicrostepsPerMM);

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
				currentSpeedX = (acceleration * time)/1000000;
			} else if(time > accelTime_usX && time <= (accelTime_usX + coastTime_usX)){
				currentSpeedX = speedX;
			} else {
				currentSpeedX = speedX - (acceleration * (time-(accelTime_usX + coastTime_usX)))/1000000;
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
				currentSpeedY = (acceleration * time)/1000000;
			} else if(time > accelTime_usY && time <= (accelTime_usY + coastTime_usY)){
				currentSpeedY = speedY;
			} else {
				currentSpeedY = speedY - (acceleration * (time-(accelTime_usY + coastTime_usY)))/1000000;
			}
			pulseLengthY = 1000000/(currentSpeedY * XYmicrostepsPerMM);
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

void moveXYAbsolute(float x, float y, float speed, float accel){
  moveXYRelative(x-currentX, y-currentY, speed, accel);
  currentX = x;
  currentY = y;
}

void moveAxisRelative(axis moveAxis, float distance, float speed, float acceleration){
	float ZmicrostepsPerMM = Z_STEPS_PER_MM * MICROSTEP_FACTOR;

	pinWrite(moveAxis,dir0, distance < 0);

	float travelDistance = fabs(distance);

	float accelTime = speed/acceleration;
	float accelDistance = calcDistance(accelTime, 0, acceleration);
	float coastDistance = travelDistance - (2*accelDistance);
	float coastTime = coastDistance/speed;

	if(coastTime < 0){
		speed = sqrt(travelDistance/acceleration);
		accelTime = speed/acceleration;
		accelDistance = calcDistance(accelTime, 0, acceleration);
		coastTime = 0;
		coastDistance = 0;
	}

	unsigned long accelTime_us = accelTime * 1000000;
	unsigned long coastTime_us = coastTime * 1000000;

	unsigned long steps = ZmicrostepsPerMM * travelDistance;
	float currentSpeed = 5;
	unsigned long pulseLength = 1000000/(currentSpeed * ZmicrostepsPerMM);

	// Time
	unsigned long time = 0;
	unsigned long pulseTimer = 0;
	unsigned long timeStep = 10;

	while(steps > 0){
		delayMicro(timeStep);
		time += timeStep;
		pulseTimer += timeStep;

		if(steps > 0 && pulseTimer >= pulseLength){
			pulseTimer = 0;
			if(time <= accelTime_us){
				currentSpeed = (acceleration * time)/1000000;
			} else if(time > accelTime_us && time <= (accelTime_us + coastTime_us)){
				currentSpeed = speed;
			} else {
				currentSpeed = speed - (acceleration * (time-(accelTime_us + coastTime_us)))/1000000;
			}
			pulseLength = 1000000/(currentSpeed * ZmicrostepsPerMM);
			pinWrite(moveAxis, step,1);
			delayMicro(10);
			pinWrite(moveAxis, step,0);
			time += 10;
			pulseTimer += 10;
			steps--;
		}
	}
}

void moveZAbsolute(float z, float speed, float acceleration){
	moveAxisRelative(Z, z-currentZ, speed, acceleration);
	currentZ = z;
}

float calcDistance(float time, float speed, float acceleration){
	return (0.5 * acceleration * pow(time,2)) + (speed * time);
}

unsigned long gcd_recurse(unsigned long a, unsigned long b) {
  if (b == 0) return a;
  if (a == 0) return b;
  if (b > a) {
    return gcd_recurse(a, b % a);
  }

  return gcd_recurse(b, a % b);
}

typedef struct point {
    unsigned int x;
    unsigned int y;
} point;

typedef struct sizeOfPiece {
    char key;
    double value;
} sizeOfPiece;

sizeOfPiece arr[8] = {{'p',44.7}, {'k',54.2}, {'r',42.1}, {'b',61.7}, {'q',73.2}, {'k',88.2}};

                    // bottom right                                                       // bottom left
point board[64] = {{78,180}, {78,221}, {78,262}, {78,303}, {78,349}, {77,385}, {77,426}, {77,466},
                   {119,181},{119,222},{118,262},{118,303},{118,345},{117,385},{116,426},{116,426},
                   {160,181},{159,221},{159,262},{158,304},{158,345},{157,385},{157,426},{157,426},
                   {199,181},{199,222},{199,222},{198,304},{198,344},{197,385},{196,426},{196,465},
                   {241,180},{241,220},{241,220},{239,303},{239,384},{239,384},{238,425},{238,465},
                   {281,180},{281,220},{281,220},{280,303},{279,383},{279,383},{278,424},{278,464},
                   {321,179},{321,220},{321,220},{320,302},{319,383},{319,383},{319,424},{318,465},
                   {361,179},{361,220},{361,220},{360,302},{360,383},{360,383},{359,424},{359,465}};
                   // top right                                                         // top left

point blackCaptured[17] = {{378,566},
                           {338,586}, {338,547},
                           {298,586}, {298,547},
                           {258,586}, {258,547},
                           {218,586}, {218,547},
                           {178,586}, {178,547},
                           {138,586}, {138,547},
                           {98,586},  {98,547},
                           {58,586},  {58,547}};


point whiteCaptured[17] = {{382,77},
                           {343,97}, {343,57},
                           {302,97}, {302,57},
                           {262,97}, {262,57},
                           {222,97}, {222,57},
                           {182,97}, {182,57},
                           {142,97}, {142,57},
                           {102,97}, {102,57},
                           {62,97},  {62,57}};




void BoardCal(){
    for(int i = 0; i < 64; i++){
        //  Send this to STM / Aurdino
        moveXYAbsolute(board[i].x,board[i].y,80,300);
    }
    for(int i = 0; i < 17; i++){
        //  Send this to STM / Aurdino
    	moveXYAbsolute(blackCaptured[i].x,blackCaptured[i].y,80,300);
    }
    for(int i = 0; i < 17; i++){
        //  Send this to STM / Aurdino
    	moveXYAbsolute(whiteCaptured[i].x,whiteCaptured[i].y,80,300);
    }
}
