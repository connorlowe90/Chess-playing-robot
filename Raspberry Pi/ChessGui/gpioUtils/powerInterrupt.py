import RPi.GPIO as GPIO
import time
from LCD_Power import*

button = 40
count = 1

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

GPIO.setup(button, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

def button_press_callback(channel):
    global count
    print("Button 2 was pressed")
    time.sleep(1)
    if(count == 1):
        power_off()
        count = 0
    else:
        power_on()
        count = 1
    
    
    
    

