from RPLCD.i2c import CharLCD
import RPi.GPIO as GPIO
import time

button = 38
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(button, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)


lcd = CharLCD(i2c_expander='PCF8574', address=0x27, port=1,
              cols=16, rows=2, dotsize=8,
              charmap='A02',
              auto_linebreaks=False,
              backlight_enabled=True)


# hint_press_callback() function is a
# function that is will tell you what
# diff you are at
def hint_press_callback(channel):
    edit_me = 'Knight to G3'
    lcd.clear()
    lcd.write_string('Best move is: \r\n' + str(edit_me))
    time.sleep(5)
    lcd.clear()
    
    
