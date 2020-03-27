import lcddriver
import time
import RPi.GPIO as GPIO
import requests
import json
import time
from hx711 import HX711
from urllib.request import urlopen

URL = "http://restservices496.herokuapp.com/containers"
id = 1
PARAMS = {'container_id':id}
r = requests.get(url = URL, params = PARAMS)
data = r.json()
print("Existing containers:")
print(data)

print("   ")

print("   ")

print("   ")

headers={'Content-type':'application/json', 'Accept':'application/json'}
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
    long_string(display, "Welcome to ZoologicalFooding Project", 1)
    display.lcd_display_string(":)", 2)
    GPIO.setmode(GPIO.BCM)

    hx = HX711(dout_pin=5, pd_sck_pin=6)

    error = hx.zero()

    if error:
        raise ValueError('Cannot tare the scale')

    reading = hx.get_raw_data_mean()
    
    if not reading:
        print('incorrect data', reading)


    
    input('Place a known weighted object')
    reading = hx.get_data_mean()
    if reading:
        known_weight_grams = input('Weight of the object: ')
        try:
            value = float(known_weight_grams)

        except ValueError:
            print('Incorrect type of value')

        ratio = reading / value
        hx.set_scale_ratio(ratio)
        print('Scaling done')
        long_string(display, "Scaling done", 1)
        time.sleep(1)
        display.lcd_display_string("                            ", 1)
        display.lcd_display_string("                            ", 2)
    else:
        raise ValueError('Cannot calculate the incoming value')


    print("Starting to measure...")
    input('Ready? (Enter)')
    URL3 = "https://restservices496.herokuapp.com/editContainer/761"
    last_time_measured = time.time()
    
    while True:
        wght = hx.get_weight_mean(20)
        print("%.2f" % wght, 'gr')
        display.lcd_display_string("Weight:", 1)
        display.lcd_display_string("                             ", 2)
        display.lcd_display_string("%5.2f gr"%wght, 2)
        
        weight = float("{0:.2f}".format(wght))
        if int(time.time() - last_time_measured) > 15:
            html = urlopen("http://ipinfo.io/json").read()
            data = json.loads(html.decode('utf-8'))
            IP=data['ip']
            org=data['org']
            city = data['city']
            country=data['country']
            region=data['region']
            loc=data['loc']
            long = loc[:loc.index(',')]
            lat = loc[loc.index(',')+1:]

            headers={'Content-type':'application/json', 'Accept':'application/json'}

            URL3 = "https://restservices496.herokuapp.com/editContainer/761"
            #data = {'name':'real container','type':'dosdsdsg','longitude':1,'latitude':1,'address':'a','weight':0, 'ip':'a','city':'a','region':'a','country':'a'}
            data = {'name':'real container','type':'dosdsdsg','longitude':long,'latitude':lat,'address':'adrsssss','weight':weight, 'ip':IP,'city':city,'region':region,'country':country}
            r3 = requests.put(url = URL3, data=json.dumps(data),headers=headers)
            

            w = str(weight)
            print("Weight : " + w + " gr , Location: " + long + ", " + lat + ", " + city + ", " + country + ", IP: " + IP + " sent to database")

            last_time_measured = time.time()

except (KeyboardInterrupt, SystemExit):
    print('The program ended')

finally:
    GPIO.cleanup()
