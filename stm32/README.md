# STM32 Motor Driver
### IAR Setup
### 1. Install IAR following the [course notes](https://docs.google.com/document/d/1H3U4RQ0HwUOEVmeoOWL-qB9FRJE-yOB3t5huG--UJWk)
 - Header files are included in the repo and do not need to be installed again

### 2. Configure IAR for the STM32F4-Discovery
 - This may already be done, try uploading to the board first
 - If that doesn't work follow [this](http://dccharacter.blogspot.com/2013/03/creating-new-project-for-stm32f4.html)


### A4988 Wiring
Make sure to set the [current limit](https://ardufocus.com/howto/a4988-motor-current-tuning/) for each driver

![Wiring Diagram](https://a.pololu-files.com/picture/0J10073.600.jpg?75d9ca5bb2e095e5c5f64350019e1b81)
