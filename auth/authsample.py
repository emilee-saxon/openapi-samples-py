import requests
from urllib.parse import urlencode
from base64 import b64encode

# Application details
app_key = ""
app_secret = ""
redirect_uri = "http://localhost/myapp"
auth_base_url = "https://sim.logonvalidation.net"  # Make sure this is correct
# Generate a random state string
state = "random_state_string"

# Step 1: Construct the authorization URL
params = {
    'response_type': 'code',
    'client_id': app_key,
    'redirect_uri': redirect_uri,
    'state': state
}

authorization_url = f"{auth_base_url}/authorize?{urlencode(params)}"
print(f"Please go to this URL to authorize the application:\n{authorization_url}")

# Step 2: Wait for the user to paste the authorization code
authorization_code = input("Enter the authorization code you received after login: ")

# Step 3: Exchange the authorization code for an access token
token_url = f"{auth_base_url}/token"
client_credentials = f"{app_key}:{app_secret}"
encoded_credentials = b64encode(client_credentials.encode()).decode()

token_data = {
    'grant_type': 'authorization_code',
    'code': authorization_code,
    'redirect_uri': redirect_uri
}

headers = {
    'Authorization': f"Basic {encoded_credentials}",
    'Content-Type': 'application/x-www-form-urlencoded'
}

response = requests.post(token_url, data=token_data, headers=headers)

if response.status_code == 201:
    access_token_info = response.json()
    access_token = access_token_info.get('access_token')
    refresh_token = access_token_info.get('refresh_token')
    print(f"\nAccess Token: {access_token}")
    print(f"Refresh Token: {refresh_token}")
else:
    print("\nFailed to obtain access token:")
    print(response.status_code, response.text)
