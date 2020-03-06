import requests
import json
import time
import random
URL = "http://restservices496.herokuapp.com/containers"
id = 1
PARAMS = {'container_id':id}
r = requests.get(url = URL, params = PARAMS)
data = r.json()
print(data)

print("   ")

print("   ")

print("   ")

headers={'Content-type':'application/json', 'Accept':'application/json'}


URL3 = "https://restservices496.herokuapp.com/editContainer/761"

last_time_measured = time.time()
while True:
    weight = float("{0:.2f}".format(random.uniform(1, 10)))
    #print to lcd
    if int(time.time() - last_time_measured) > 10:
        data = {'name':'real container','type':'dosdsdsg','longitude':'12221','latitude':'114244','address':'adrsssss','weight':weight}
        r3 = requests.put(url = URL3, data=json.dumps(data),headers=headers)
        pastebin_url2 = r3.text 
        print("The pastebin URL is:%s"%pastebin_url2) 
        print(weight)
        last_time_measured = time.time()
