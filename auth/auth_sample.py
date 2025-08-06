"""
OAuth 2.0 Authorization Code Flow Server
=================================================================


This script sets up a simple HTTP server to facilitate OAuth 2.0 authorization code flow.
It redirects users to an authorization endpoint, receives the authorization code,
exchanges it for access and refresh tokens, and demonstrates token renewal.

Setup Instructions:
- Create a `.env` file in the same directory with the following variables:
    AppKey=your_app_key_here
    AppSecret=your_app_secret_here
    RedirectUrl=http://localhost:3000/callback
    AuthorizationUrl=https://example.com/oauth/authorize
    TokenUrl=https://example.com/oauth/token

How It Works:
- The server uses the `RedirectUrl` to determine:
    1. The port it should run on (e.g., `3000` from `http://localhost:3000/callback`).
    2. The path it should listen for (e.g., `/callback`)
- If no port is specified in the redirect URL, the server defaults to port `80`.



A demo template is provided as `.env.example` to help you get started quickly.
You can copy it using: `cp .env.example .env` and fill in your credentials.


"""



import os
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs, urlencode
from base64 import b64encode
import requests
from dotenv import load_dotenv
import time


# Load and validate environment variables
def load_config(app=None):
    if app:
        return app

    load_dotenv()

    required_keys = ["AppKey", "AppSecret", "AuthorizationUrl", "TokenUrl", "RedirectUrl"]
    config = {key: os.getenv(key) for key in required_keys}

    missing = [key for key, value in config.items() if not value]
    if missing:
        raise EnvironmentError(
            f"Missing or invalid environment variables: {', '.join(missing)}. "
            "Please check your .env file or provide a valid app config."
        )

    # Validate and extract port from redirect URL
    parsed = urlparse(config["RedirectUrl"])
    print(config)
    # Ensure path is not root
    if not parsed.path or parsed.path == "/":
        raise ValueError(f"Redirect URL '{config['RedirectUrl']}' must include a non-root path (e.g., /callback).")

    # Determine port: use from URL if present, else default to 80
    port = parsed.port or 80
    config["PORT"] = port

    if not parsed.port:
        print(f"[INFO] No port specified in redirect URL. Defaulting to port {port}.")
    else:
        print(f"[INFO] Using port {port} from redirect URL.")

    # Log final config (excluding secrets)
    print(f"[INFO] Loaded config with redirect URL: {config['RedirectUrl']}")
    print(f"[INFO] Authorization URL: {config['AuthorizationUrl']}")
    print(f"[INFO] Token URL: {config['TokenUrl']}")

    return {
        "APP_KEY": config["AppKey"],
        "APP_SECRET": config["AppSecret"],
        "REDIRECT_URL": config["RedirectUrl"],
        "AUTHORIZATION_URL": config["AuthorizationUrl"],
        "TOKEN_URL": config["TokenUrl"],
        "PORT": config["PORT"],
    }

config = load_config()

# Construct full authorization URL
FULL_AUTH_URL = f"{config['AUTHORIZATION_URL']}?response_type=code&client_id={config['APP_KEY']}&redirect_uri={config['REDIRECT_URL']}"

print(f"[INFO] Full authorization URL: {FULL_AUTH_URL}")
unpacked_response = {}

class OAuthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        global unpacked_response
        parsed_path = urlparse(self.path)
        path = parsed_path.path

        if path == "/":
            print(f"\n[INFO] Redirecting to authorization endpoint: {FULL_AUTH_URL}")
            self.send_response(302)
            self.send_header("Location", FULL_AUTH_URL)
            self.end_headers()

        elif path == urlparse(config["REDIRECT_URL"]).path:
            print("\n[INFO] Requesting tokens...")
            unpacked_response = self.get_tokens(parsed_path)

            print("[INFO] Token response:")
            print(unpacked_response)
            print("[INFO] Will refresh tokens before they expire...")

            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"Tokens received and refreshed. Check console output.")

            unpacked_response = self.renew_tokens()
            print("[INFO] Refresh response:")
            print(unpacked_response)

    def get_tokens(self, parsed_path):
        query = parse_qs(parsed_path.query)
        code = query.get("code", [None])[0]

        if not code:
            raise ValueError("Authorization code not found in callback URL.")

        data = {
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": config["REDIRECT_URL"],
        }

        return self.token_request(data)

    def renew_tokens(self):
        refresh_token = unpacked_response.get("refresh_token")
        auth_token_expiry = unpacked_response.get("expires_in")

        renew_time = auth_token_expiry - 60  # Renew 60 seconds before expiry

        if not refresh_token:
            raise ValueError("Missing refresh_token in unpacked_response. Cannot renew tokens.")

        data = {
            "grant_type": "refresh_token",
            "refresh_token": refresh_token,
            "redirect_uri": config["REDIRECT_URL"],
        }

        # refresh tokens before they expire
        while True:
            time.sleep(renew_time)
            print("[INFO] Attempting to renew tokens...")
            renewed = self.token_request(data)
            print("[INFO] Renewed token response:")
            print(renewed)
            # Optionally break if token is expired or renewal fails
            if not renewed.get("refresh_token") or renewed.get("expires_in", 0) <= 0:
                print("[INFO] Token renewal stopped: no valid refresh_token or token expired.")
                break
        
        return self.token_request(data)

    def token_request(self, data):
        basic_token = b64encode(f"{config['APP_KEY']}:{config['APP_SECRET']}".encode()).decode()
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Authorization": f"Basic {basic_token}",
        }

        response = requests.post(config["TOKEN_URL"], headers=headers, data=urlencode(data))
        try:
            return response.json()
        except Exception as e:
            raise ValueError(f"Failed to parse token response: {e}")

# Start the server using the port derived from the redirect URL
def run(server_class=HTTPServer, handler_class=OAuthHandler):


    port = config["PORT"]
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f"[INFO] Server is running on port {port}")
    httpd.serve_forever()

if __name__ == "__main__":
    run()


