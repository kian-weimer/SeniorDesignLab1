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
        
        self.lcd_columns = 16
        self.lcd_rows = 2
        self.lcd_rs = digitalio.DigitalInOut(board.D26)
        self.lcd_en = digitalio.DigitalInOut(board.D19)
        self.lcd_d7 = digitalio.DigitalInOut(board.D27)
        self.lcd_d6 = digitalio.DigitalInOut(board.D22)
        self.lcd_d5 = digitalio.DigitalInOut(board.D24)
        self.lcd_d4 = digitalio.DigitalInOut(board.D25)
        self.lcd = characterlcd.Character_LCD_Mono(self.lcd_rs, self.lcd_en, self.lcd_d4, self.lcd_d5, self.lcd_d6, self.lcd_d7, self.lcd_columns, self.lcd_rows)
        self.unplugged = False

    def get_and_print_temp_on(self):
        temp = ThermometerCode.get_temp()
        print(temp)
        if type(temp) != int and not temp:
            self.lcd.clear()
            self.lcd.message = "The Temp Sensor\nis Unplugged"
            self.unplugged = True
            return False
        else:
            if(self.unplugged):
                self.lcd.clear()
                self.lcd = characterlcd.Character_LCD_Mono(self.lcd_rs, self.lcd_en, self.lcd_d4, self.lcd_d5, self.lcd_d6, self.lcd_d7, self.lcd_columns, self.lcd_rows)
                self.unplugged = False
            self.lcd.clear()
            self.lcd.message = "{:10.2f}C".format(temp)
            return temp
    
    @staticmethod
    def on(on):
        if(on):
            GPIO.output(13, 1)
            GPIO.output(6, 0)
        else:
            GPIO.output(13, 0)
            GPIO.output(6, 1)
