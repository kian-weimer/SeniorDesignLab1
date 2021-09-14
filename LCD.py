import adafruit_character_lcd.character_lcd as characterlcd
import board
import digitalio
import ThermometerCode

class LCD:

    def __init__(self):
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
        self.lcd.clear()
        self.lcd.message = "{:10.2f}".format(temp)
        
    
