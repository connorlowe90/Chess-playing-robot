import RPi.GPIO as GPIO
import time

# lcd = CharLCD(i2c_expander='PCF8574', address=0x27, port=1,
#               cols=16, rows=2, dotsize=8,
#               charmap='A02',
#               auto_linebreaks=False,
#               backlight_enabled=True)

# setup_LEDs() function will
# set up the pins and PWM for
# the RGB LED
def setup_LEDs():
    global potR, potG, potB
    rgb = [33, 35, 37]
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(rgb, GPIO.OUT)
    potR = GPIO.PWM(rgb[0], 100)
    potG = GPIO.PWM(rgb[1], 100)
    potB = GPIO.PWM(rgb[2], 100)
    potR.start(100)
    potG.start(100)
    potB.start(100)
    
# stop_LED() will stop the PWM for
# the RGB LED pins
def stop_LED():
    potR.stop()
    potG.stop()
    potB.stop()

# illegal_move() function will print
# Illegal move to the LCD and flash
# the LED red and blue
def illegal_LED():
    for i in range(0, 3):
        red_LED()
        time.sleep(0.7)
        blue_LED()
        time.sleep(0.7)
    no_LED()

# winner() function will flash
# the LED with the color green
def winner():
    for i in range(0, 4):
        green_LED()
        time.sleep(0.7)
        no_LED()
        time.sleep(0.7)

# loser() function will flash
# the LED with the color orange for
# 0.7s on, 0.7s 
def loser():
    for i in range(0, 4):
        red_LED()
        time.sleep(0.7)
        no_LED()
        time.sleep(0.7)

# user_in_check() function will flash
# the LED with the color orange for
# 0.7s on, 0.7s 
def user_in_check():
    for i in range(0, 4):
        orange_LED()
        time.sleep(0.7)
        no_LED()
        time.sleep(0.7)

# comp_in_check() function will flash
# the LED with the color purple
def comp_in_check():
    for i in range(0, 4):
        purple_LED()
        time.sleep(0.7)
        no_LED()
        time.sleep(0.7)

# got_a_draw() function will flash
# the LED with the color cyan
def got_a_draw():
    for i in range(0, 4):
        cyan_LED()
        time.sleep(0.7)
        no_LED()
        time.sleep(0.7)

# stalemate() function will flash
# the LED with the colors light
# pink and orange
def stalemate():
    for i in range(0, 4):
        light_pink_LED()
        time.sleep(0.7)
        orange_LED()
        time.sleep(0.7)
    no_LED()
    
#********************************
# Different assortment of LED
# color functions as well as no
# LED on funtion
#********************************
def red_LED():
    potR.ChangeDutyCycle(0)
    potG.ChangeDutyCycle(100)
    potB.ChangeDutyCycle(100)

def blue_LED():
    potR.ChangeDutyCycle(100)
    potG.ChangeDutyCycle(100)
    potB.ChangeDutyCycle(0)

def yellow_LED():
    potR.ChangeDutyCycle(0)
    potG.ChangeDutyCycle(0)
    potB.ChangeDutyCycle(100)

def green_LED():
    potR.ChangeDutyCycle(100)
    potG.ChangeDutyCycle(0)
    potB.ChangeDutyCycle(100)

def purple_LED():
    potR.ChangeDutyCycle(0)
    potG.ChangeDutyCycle(100)
    potB.ChangeDutyCycle(0)

def orange_LED():
    potR.ChangeDutyCycle(0)
    potG.ChangeDutyCycle(75)
    potB.ChangeDutyCycle(100)

def cyan_LED():
    potR.ChangeDutyCycle(92)
    potG.ChangeDutyCycle(0)
    potB.ChangeDutyCycle(0)
    
def light_pink_LED():
    potR.ChangeDutyCycle(0)
    potG.ChangeDutyCycle(70)
    potB.ChangeDutyCycle(55)
    
def no_LED():
    potR.ChangeDutyCycle(100)
    potG.ChangeDutyCycle(100)
    potB.ChangeDutyCycle(100)
