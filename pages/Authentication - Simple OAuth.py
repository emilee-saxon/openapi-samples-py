import streamlit as st
import requests
from urllib.parse import urlencode, urlparse, parse_qs
from base64 import b64encode

st.set_page_config(page_title="Authentication", page_icon="🔐")

st.title("OAuth2 Authorization Flow Demo")

with st.expander("How OAuth2 Works"):
    st.markdown("""
    OAuth2 Flow Overview:
    1. Enter your app credentials and endpoints.
    2. Click the button to start the OAuth2 flow.
    3. Complete login and authorization in the new browser tab.
    4. After redirection, copy the full URL from the browser's address bar.
    5. Paste the URL below to extract the authorization code.
    6. Use the code to request access and refresh tokens.
    """)

# Step 0: User Inputs
st.subheader("Step 0: Enter OAuth2 Configuration")

APP_KEY = st.text_input("App Key")
APP_SECRET = st.text_input("App Secret", type="password")
REDIRECT_URL = st.text_input("Redirect URL", value="http://localhost:3000/callback")
AUTHORIZATION_URL = st.text_input("Authorization URL")
TOKEN_URL = st.text_input("Token URL")

def token_request(data):
    basic_token = b64encode(f"{APP_KEY}:{APP_SECRET}".encode()).decode()
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Authorization": f"Basic {basic_token}",
    }
    response = requests.post(TOKEN_URL, headers=headers, data=urlencode(data))
    return response

def get_tokens(parsed_path):
    query = parse_qs(parsed_path.query)
    code = query.get("code", [None])[0]
    data = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": REDIRECT_URL,
    }
    return token_request(data)

if APP_KEY and APP_SECRET and REDIRECT_URL and AUTHORIZATION_URL and TOKEN_URL:
    params = {
        "response_type": "code",
        "client_id": APP_KEY,
        "redirect_uri": REDIRECT_URL,
    }
    auth_url = f"{AUTHORIZATION_URL}?{urlencode(params)}"

    # Step 1: Start Authorization
    st.subheader("Step 1: Start Authorization")
    if st.button("Authorize", key="authorize_button"):
        st.markdown(f'<a href="{auth_url}" target="_blank">Click here to authorize</a>', unsafe_allow_html=True)

    # Step 2: Extract Code from Redirect URL
    st.subheader("Step 2: Extract Authorization Code from Redirect URL")
    redirect_url = st.text_input("Paste the full redirect URL here:")
    parsed_path = urlparse(redirect_url) if redirect_url else None
    code = None
    if parsed_path:
        code = parse_qs(parsed_path.query).get("code", [None])[0]
        if code:
            st.success("Authorization code extracted ✔️")
            st.write("Code:", code)
        else:
            st.error("No authorization code found in the URL.")

    # Step 3: Exchange Code for Tokens
    st.subheader("Step 3: Exchange Authorization Code for Tokens")
    if st.button("Get Tokens", key="get_token_button") and parsed_path:
        response = get_tokens(parsed_path)
        if response.status_code == 201:
            tokens = response.json()
            st.success("Tokens received successfully ✔️")
            st.json(tokens)
        else:
            st.error("Failed to retrieve tokens.")
            st.text(response.text)

    # Step 4: Refresh Token
    st.subheader("Step 4: Refresh Access Token")
    refresh_token = st.text_input("Paste your refresh token here:")

    if st.button("Refresh Token", key="refresh_token_button") and refresh_token:
        data = {
            "grant_type": "refresh_token",
            "refresh_token": refresh_token,
            "redirect_uri": REDIRECT_URL,
        }
        response = token_request(data)
        if response.status_code == 201:
            refreshed_tokens = response.json()
            st.success("Token refreshed successfully ✔️")
            st.json(refreshed_tokens)
        else:
            st.error("Failed to refresh token.")
            st.text(response.text)
else:
    st.warning("Please fill in all configuration fields to proceed.")




# Read code from file
with open("auth/auth_sample.py", "r") as file:
    code_body = file.read()


# Display with title and expandable section
with st.expander("🔐 Full Code Example", expanded=False):
    st.code(code_body, language="python", line_numbers=True)
