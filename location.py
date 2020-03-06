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
