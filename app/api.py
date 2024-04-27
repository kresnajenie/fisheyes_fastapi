import requests


url = 'https://fisheyes.techkyra.com/savedata'
data = {'key': 'genes', 'value': 'test'}

response = requests.post(url, json=data)
print(response.json())
