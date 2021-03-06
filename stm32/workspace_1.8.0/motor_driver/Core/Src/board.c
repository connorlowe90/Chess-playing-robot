// Kellen Hartnett
// Adrian Lewis
// Connor Lowe
// Sahibjeet Singh
// Garrett Tashiro
// EE 475, Group 5 Capstone Project

#include "board.h"
#include "main.h"
// For the STM32 board

/*

 X step pin = PC14
 X dir0 pin = PC15
 X dir1 pin = PC13

 Y step pin = PC5
 Y dir0 pin = PA1
 Y dir1 pin = PA2

 Z step pin = PA3
 Z dir0 pin = PA3

 */

// Initialize all pins and timers needed
void initPins(){
  TIM6->PSC = 89;
  TIM6->ARR = 0xffff;
  TIM6->CR1 |= (1 << 0);
}

// Write to a pin for a given axis
void pinWrite(axis writeAxis, pin writePin, int state){
	int shift = state * 16;
  switch(writeAxis){
    case X:
      switch(writePin){
        case step:
        	GPIOC->BSRR |= (1<<14) << shift;
          break;
        case dir0:
        	GPIOC->BSRR |= (1<<15) << shift;
          break;
        case dir1:
        	GPIOC->BSRR |= (1<<13) << shift;
          break;
      }
      break;
      case Y:
      switch(writePin){
        case step:
        	GPIOC->BSRR |= (1<<5) << shift;
          break;
        case dir0:
        	GPIOA->BSRR |= (1<<1) << shift;
          break;
        case dir1:
        	GPIOA->BSRR |= (1<<2) << shift;
          break;
      }
      break;
      case Z:
		switch(writePin){
		  case step:
			GPIOA->BSRR |= (1<<5) << shift;
			break;
		  case dir0:
			GPIOA->BSRR |= (1<<3) << shift;
			break;
		  case dir1:
			break;
		}
		break;
  }
}

// Turn the electromagnet on or off
void setMagnet(int state){
	int shift = state * 16;
	GPIOE->BSRR |= (1<<9) << shift;
}

// Delays a given amount of microseconds (blocking)
void delayMicro(long time){
	TIM6->CNT = 0;
	while(TIM6->CNT < time){}
}

