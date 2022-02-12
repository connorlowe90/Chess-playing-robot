#include "motor.h"

#define BUFFER_SZ 16
static char buffer[BUFFER_SZ];
static size_t lg = 0;
int speed = 80;
int accel = 20;

void setup() {
  // put your setup code here, to run once:
  initPins();
  Serial.println("ON");
}

void parse(char *buffer){
  if(buffer[0] == 'a'){
    char *s = strtok(buffer, "=");
    s = strtok(NULL, "=");
    accel = atoi(s);
    Serial.print("Acceleration is set to ");
    Serial.println(accel);
  } else if(buffer[0] == 's'){
    char *s = strtok(buffer, "=");
    s = strtok(NULL, "=");
    speed = atoi(s);
    Serial.print("Speed is set to ");
    Serial.println(speed);
  } else if(buffer[0] == 'p'){
    int amount = buffer[1];
    Serial.print("Performing pattern ");
    Serial.print(amount);
    Serial.println(" times");
    for(int i = 0; i<amount; i++){
      doPattern();
    }
    Serial.println("Pattern(s) Done");
  } else if(buffer[0] == 'h'){
    setHome();
    Serial.println("Home set");
  } else {
    char *s = strtok(buffer, ",");
    int x = atoi(s);
    s = strtok(NULL, ",");
    int y = atoi(s);
    moveXYAbsolute(x,y,speed,accel);
    Serial.println("Move Complete");
  }
}

void doPattern(){
  moveXYAbsolute(MACHINE_BOUND_X/2,0,speed,accel);
  moveXYAbsolute(MACHINE_BOUND_X,MACHINE_BOUND_Y/2,speed,accel);
  moveXYAbsolute(MACHINE_BOUND_X/2,MACHINE_BOUND_Y,speed,accel);
  moveXYAbsolute(0,MACHINE_BOUND_Y/2,speed,accel);
}

void loop(){
    while (Serial.available()) {
        char c = Serial.read();
        if (c == '\n') {        // carriage return
            buffer[lg] = '\0';  // terminate the string
            parse(buffer);
            lg = 0;             // get ready for next message
        }
        else if (lg < BUFFER_SZ - 1) {
            buffer[lg++] = c;
        }
    }
}
