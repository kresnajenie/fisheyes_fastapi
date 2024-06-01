import requests
import json


url = 'http://localhost:8000/savedata'
# url = 'https://fisheyes.techkyra.com/savedata'
collection = "50pe"
key = "genes"

data = {'collection': collection, 'key': key, 'values': json.dumps(genes)}

response = requests.post(url, json=data)
print(response.json())
