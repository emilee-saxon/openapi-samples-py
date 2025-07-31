"""
OAuth 2.0 Authorization Code Flow with PKCE – Local Server Script
=================================================================

This script sets up a local HTTP server to support the OAuth 2.0 Authorization Code Flow
with Proof Key for Code Exchange (PKCE). It's designed for development and testing purposes,
allowing you to authenticate and retrieve tokens from an OAuth provider using a local redirect URI.

What it does:

- Loads configuration from environment variables:
  AppKey, RedirectUrl, AuthorizationEndpoint, and TokenUrl.
- Parses the redirect URI to extract the port and path.
- Generates a PKCE code verifier and challenge.
- Constructs the authorization URL and starts a local HTTP server.
- Redirects to the authorization endpoint.
- Handles the redirect back with the authorization code.
- Exchanges the code for access and refresh tokens.
- Prints token responses to the console.

How to use it:

1. Set the required environment variables in a `.env` file or your shell.
2. Run the script:
       python3 auth_sample_PKCE.py
3. Open a browser and go to `http://localhost:<PORT>/` to start the flow.

Important:

- The `RedirectUrl` must include a non-root path (e.g., `/callback`).
- Running on port 80 requires root privileges:
      sudo python3 oauth_pkce_server.py


"""






import os
import base64
import hashlib
import secrets
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs, urlencode
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


# Required environment variables
required_keys = ["AppKey", "RedirectUrl", "AuthorizationEndpoint", "TokenUrl"]
config = {key: os.getenv(key) for key in required_keys}

# Validate environment variables
missing = [key for key, value in config.items() if not value]
if missing:
    raise EnvironmentError(f"Missing environment variables: {', '.join(missing)}")

# Extract port and path from RedirectUrl
parsed = urlparse(config["RedirectUrl"])
if not parsed.path or parsed.path == "/":
    raise ValueError("RedirectUrl must include a non-root path (e.g., /callback)")

#Extract port, otherwise we set to 80 
port = parsed.port or 80
config["PORT"] = port
config["REDIRECT_PATH"] = parsed.path

# Generate PKCE code_verifier and code_challenge
def generate_pkce_pair():
    code_verifier = base64.urlsafe_b64encode(secrets.token_bytes(32)).rstrip(b'=').decode('utf-8')
    code_challenge = base64.urlsafe_b64encode(
        hashlib.sha256(code_verifier.encode('utf-8')).digest()
    ).rstrip(b'=').decode('utf-8')
    return code_verifier, code_challenge

code_verifier, code_challenge = generate_pkce_pair()
state = secrets.token_urlsafe(16)

# Construct authorization URL
authorization_url = (
    f"{config['AuthorizationEndpoint'].rstrip('/')}?"
    f"response_type=code&client_id={config['AppKey']}&redirect_uri={config['RedirectUrl']}"
    f"&state={state}&code_challenge={code_challenge}&code_challenge_method=S256"
)


print(f"[INFO] Authorization URL:\n{authorization_url}")

# Token endpoint
token_url = f"{config['TokenUrl'].rstrip('/')}"

# HTTP handler
class OAuthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urlparse(self.path)
        if parsed_path.path == "/":
            self.send_response(302)
            self.send_header("Location", authorization_url)
            self.end_headers()
        elif parsed_path.path == config["REDIRECT_PATH"]:
            query = parse_qs(parsed_path.query)
            code = query.get("code", [None])[0]
          
            if not code:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(b"Missing authorization code.")
                return

            # Exchange code for tokens
            data = {
                "grant_type": "authorization_code",
                "client_id": config["AppKey"],
                "code": code,
                "redirect_uri": config["RedirectUrl"],
                "code_verifier": code_verifier
            }
            headers = {"Content-Type": "application/x-www-form-urlencoded"}
      
            response = requests.post(token_url, headers=headers, data=urlencode(data))

        
            token_response = response.json()
            print("[INFO] Token response:")
            print(token_response)

            print("\n")
            print("\n")

            # Refresh token if available
            refresh_token = token_response.get("refresh_token")
            if refresh_token:
                refresh_data = {
                    "grant_type": "refresh_token",
                    "refresh_token": refresh_token,
                    "client_id": config["AppKey"],
                    "code_verifier": code_verifier
                }
                refresh_response = requests.post(token_url, headers=headers, data=urlencode(refresh_data))
                print("[INFO] Refresh token response:")
                print(refresh_response.json())

            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"Authorization complete. Check console for token details.")

# Run server
def run():
    server_address = ('', config["PORT"])
    httpd = HTTPServer(server_address, OAuthHandler)
    print(f"[INFO] Server running on port {config['PORT']}")
    httpd.serve_forever()

if __name__ == "__main__":
    run()
