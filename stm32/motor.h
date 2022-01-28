#ifndef Motor_h
#define Motor_h
// Header stuff goes here

#define x-axis 1
#define y-axis 2
#define z-axis 3

void motors_init();

void move_motor(byte axis, byte dir, byte speed);

void stop_motor(byte axis);

#endif