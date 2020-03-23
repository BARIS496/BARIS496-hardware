import lcddriver
import time
import RPi.GPIO as GPIO
from hx711 import HX711

display = lcddriver.lcd()

try:

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
        time.sleep(1)
        display.lcd_display_string("                            ", 1)
        display.lcd_display_string("                            ", 2)
    else:
        raise ValueError('Gelen deger hesaplanamiyor')


    print("Surekli olarak olculen deger aktarilacak")
    input('Baslamak icin enter\'a basin')

    while True:
        wght = hx.get_weight_mean(20)
        print("%.2f" % wght, 'gr')
        display.lcd_display_string("Kutle:", 1)
        display.lcd_display_string("                             ", 2)
        display.lcd_display_string("%5.2f gr"%wght, 2)

except (KeyboardInterrupt, SystemExit):
    print('program sonlandi')

finally:
    GPIO.cleanup()
