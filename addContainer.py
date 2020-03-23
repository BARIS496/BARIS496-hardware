import requests
import json
headers={'Content-type':'application/json', 'Accept':'application/json'}

URL2 = "https://restservices496.herokuapp.com/addContainer"

data = {'name':'presentation','type':'dosdsdsg','longitude':1,'latitude':1,'address':'adrsssss','weight':0.0, 'ip':'1','city':'a','region':'a','country':'a'}
r2 = requests.post(url = URL2, data=json.dumps(data),headers=headers)
pastebin_url = r2.text 
print("The pastebin URL is:%s"%pastebin_url) 

