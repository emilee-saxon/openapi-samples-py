import requests


access_token = ""
url = 'https://gateway.saxobank.com/sim/openapi/port/v1/clients/me'

headers = {
    'Authorization': f'Bearer {access_token}',
    'Accept': 'application/json'
}

print(headers)
response = requests.get(url, headers=headers)

if response.status_code == 200:
    print(response.json())
else:
    print(f"Error {response.status_code}: {response.text}")
