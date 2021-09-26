import adafruit_character_lcd.character_lcd as characterlcd
import board
import digitalio
import ThermometerCode
import RPi.GPIO as GPIO

class LCD:
    
    website_on = False
    
    def __init__(self):
        
        GPIO.setup(13, GPIO.OUT) #for turning on and off the LCD
        GPIO.output(13, 0)
        GPIO.setup(6, GPIO.OUT) #for turning on and off the LCD
        GPIO.output(6, 1)
        
        lcd_columns = 16
        lcd_rows = 2
        lcd_rs = digitalio.DigitalInOut(board.D26)
        lcd_en = digitalio.DigitalInOut(board.D19)
        lcd_d7 = digitalio.DigitalInOut(board.D27)
        lcd_d6 = digitalio.DigitalInOut(board.D22)
        lcd_d5 = digitalio.DigitalInOut(board.D24)
        lcd_d4 = digitalio.DigitalInOut(board.D25)
        lcd_columns = 16
        lcd_rows = 2
        self.lcd = characterlcd.Character_LCD_Mono(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7, lcd_columns, lcd_rows)

    def get_and_print_temp_on(self):
        temp = ThermometerCode.get_temp()
        if type(temp) != int and not temp:
            self.lcd.message = "The Temp Sensor\nis Unplugged"

            return False
        else:
            self.lcd.clear()
            self.lcd.message = "{:10.2f}".format(temp)
            return temp
    
    @staticmethod
    def on(on):
        if(on):
            GPIO.output(13, 1)
            GPIO.output(6, 0)
        else:
            GPIO.output(13, 0)
            GPIO.output(6, 1)
