import requests

x = requests.delete('https://restservices496.herokuapp.com/deleteContainer/811')

print(x.text)