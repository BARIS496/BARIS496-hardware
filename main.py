import lcddriver
import time
import RPi.GPIO as GPIO
from hx711 import HX711
display = lcddriver.lcd()
#this func will be used if needed
def long_string(display, text = '', num_line = 1, num_cols = 20):
    if(len(text) > num_cols):
        display.lcd_display_string(text[:num_cols],num_line)
        time.sleep(1)
        for i in range(len(text) - num_cols + 5):
            text_to_print = text[i:i+num_cols]
            display.lcd_display_string(text_to_print,num_line)
            time.sleep(0.2)
    else:
        display.lcd_display_string(text,num_line)
        display = lcddriver.lcd()
try:
 #   long_string(display, "Welcome to ZoologicalFooding project", 1)
  #  display.lcd_display_string(":)", 2)
    GPIO.setmode(GPIO.BCM)

    hx = HX711(dout_pin=5, pd_sck_pin=6)

    error = hx.zero()

    if error:
        raise ValueError('Tara alinamadi')

    reading = hx.get_raw_data_mean()
    
    if not reading:
        print('hatali veri', reading)


    input('Agirligi bilinen bir deger koyup enter\' a basin')
    reading = hx.get_data_mean()
    if reading:
        known_weight_grams = input('koydugunuz cismin agirligi:')
        try:
            value = float(known_weight_grams)

        except ValueError:
            print('Yanlis tip deger girildi')

        ratio = reading / value
        hx.set_scale_ratio(ratio)
        print('Olceklendirme tamamlandi')
    else:
        raise ValueError('Gelen deger hesaplanamiyor')


    print("Surekli olarak olculen deger aktarilacak")
    input('Baslamak icin enter\'a basin')
    while True:
       # print("%.2f" % hx.get_weight_mean(20), 'gr')
        display.lcd_display_string("%5.2f gr"%hx.get_weight_mean(20), 2)

except (KeyboardInterrupt, SystemExit):
    print('program sonlandi')

finally:
    GPIO.cleanup()
