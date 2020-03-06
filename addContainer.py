import requests
import json
headers={'Content-type':'application/json', 'Accept':'application/json'}

URL2 = "https://restservices496.herokuapp.com/addContainer"

data = {'name':'real container','type':'dosdsdsg','lng':12221,'lat':114244,'address':'adrsssss','weight':0.0}
r2 = requests.post(url = URL2, data=json.dumps(data),headers=headers)
pastebin_url = r2.text 
print("The pastebin URL is:%s"%pastebin_url) 