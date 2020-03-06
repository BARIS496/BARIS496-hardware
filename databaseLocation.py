import requests
import json
from urllib.request import urlopen
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

data = {'name':'real container','type':'dosdsdsg','longitude':long,'latitude':lat,'address':'adrsssss','weight':0.0, 'ip':IP,'city':city,'region':region,'country':country}
r3 = requests.put(url = URL3, data=json.dumps(data),headers=headers)
pastebin_url2 = r3.text 
print("The pastebin URL is:%s"%pastebin_url2) 