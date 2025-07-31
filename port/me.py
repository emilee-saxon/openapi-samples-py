import requests


access_token = "eyJhbGciOiJFUzI1NiIsIng1dCI6IjczMEZDMUQwMUQ0MzM5Q0JGRTU3MTc0Q0NGREQ0RjExRDZENzgwNDYifQ.eyJvYWEiOiI3Nzc3MCIsImlzcyI6Im9hIiwiYWlkIjoiMTkzNyIsInVpZCI6IjZ2M3dHfElpQ0VBRk40NG5BY2kyR3c9PSIsImNpZCI6IjZ2M3dHfElpQ0VBRk40NG5BY2kyR3c9PSIsImlzYSI6IkZhbHNlIiwidGlkIjoiMzkxNyIsInNpZCI6IjcxNTk1ZGJiMzU2MzQzNDI5MDg2MGUwZjI1ZWY4Mjg2IiwiZGdpIjoiODQiLCJleHAiOiIxNzUzNzc4ODI5Iiwib2FsIjoiMUYiLCJpaWQiOiI0NjAxZWZiNzdiNDI0MjI1NjQ5MDA4ZGI5NTZkYjBlOCJ9.S4nR4OZ-3-NoSdwOqsqefF3r9KxgcELyHOSnUUsHI_eDYn0j4rLoyDrNdnhhZU-6oI_oi5Ut3YkumgrzgDrOTg"
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
