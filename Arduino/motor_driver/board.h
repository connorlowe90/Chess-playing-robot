#ifndef Board_h
#define Board_h
// Header stuff goes here

typedef enum{X,Y,Z} axis;
typedef enum{step,dir0,dir1} pin;

// Initialize all pins and modules needed
void initPins();

// Write to a pin for a given axis
void pinWrite(axis writeAxis, pin writePin, int state);

// Delays a given amount of microseconds (blocking)
void delayMicro(long time);

#endif
