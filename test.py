import requests

BASE = "http://127.0.0.1:5000/"


response = requests.put(BASE + "car/1", {"brand": "toyota", "version": 2, "year": 2005})
print(response.json())
input()
response = requests.get(BASE + "car/1")
print(response.json())
input()
response = requests.delete(BASE + "car/1")
print(response)
input()
response = requests.get(BASE + "car/1")
print(response.json())


