import requests

x = requests.delete('https://restservices496.herokuapp.com/deleteContainer/2511')

print(x.text)