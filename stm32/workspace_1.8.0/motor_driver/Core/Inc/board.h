// Kellen Hartnett
// Adrian Lewis
// Connor Lowe
// Sahibjeet Singh
// Garrett Tashiro
// EE 475, Group 5 Capstone Project

/*
 * board.h
 * Defines board-specific commands (delays and pins)
 */

#ifndef Board_h
#define Board_h

typedef enum{X,Y,Z} axis;
typedef enum{step,dir0,dir1} pin;

// Initialize all pins and timers needed
void initPins();

// Write to a pin for a given axis
void pinWrite(axis writeAxis, pin writePin, int state);

// Turn the electromagnet on or off
void setMagnet(int state);

// Delays a given amount of microseconds (blocking)
void delayMicro(long time);

#endif
