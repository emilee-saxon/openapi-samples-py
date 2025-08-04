import requests
from datetime import datetime




def get_user(api_url="", bearer_token=""):



    # Prompt for API URL if not provided
    if not api_url:
        api_url = input("Enter the OpenAPI base URL (press Enter to use default): ").strip()
        if not api_url:
            api_url = "https://gateway.saxobank.com/sim/openapi"
            print(f"Using default URL: {api_url}")

    # Prompt for Bearer Token if not provided
    if not bearer_token:
        bearer_token = input("Enter your Bearer Token: ").strip()


    url = f"{api_url}/port/v1/users/me"
    headers = {
        "Authorization": f"Bearer {bearer_token}"
    }

    try:
        response = requests.get(url, headers=headers)
        req_info = f"Request:\nGET {response.url} status {response.status_code} {response.reason}"

        if response.ok:
            response_json = response.json()
            last_login_utc = response_json.get("LastLoginTime").rstrip('Z')
            last_login_local = datetime.fromisoformat(last_login_utc).astimezone().strftime('%Y-%m-%d %H:%M:%S')

            rep_info = f"\n\nResponse: {response_json}"
            log_message = (
                f"\n\nFound user with clientKey {response_json.get('ClientKey')} "
                f"\nLast login @ {last_login_local}.\n\n"
            )
            print(log_message + req_info + rep_info)
        else:
            print(f"Error: {response.status_code} - {response.text}")

    except Exception as e:
        print(f"Exception occurred: {e}")


get_user()
#get_user("https://gateway.saxobank.com/sim/openapi/", "eyJhbGciOiJFUzI1NiIsIng1dCI6IjI3RTlCOTAzRUNGMjExMDlBREU1RTVCOUVDMDgxNkI2QjQ5REEwRkEifQ.eyJvYWEiOiI3Nzc3MCIsImlzcyI6Im9hIiwiYWlkIjoiNjYyMSIsInVpZCI6IjBZakxGMVktSktjU3NOVGhSekVFVEE9PSIsImNpZCI6IjBZakxGMVktSktjU3NOVGhSekVFVEE9PSIsImlzYSI6IkZhbHNlIiwidGlkIjoiMTE2NDgiLCJzaWQiOiI1MGRiMzc2MTg4NjQ0NDhkODVmOGRhZWM3ZGRmYTBjNSIsImRnaSI6Ijg0IiwiZXhwIjoiMTc1NDMxMDQ3NiIsIm9hbCI6IjFGIiwiaWlkIjoiZWZmMzVlNzMxYWU4NDBmNTljZDAwOGRkNzEwMDk5NDAifQ.DuAXnnYs8uatxnxWbEKv7xkk2V-GjQ-q0GPwvmkoHHGW0OUpzgUER5o_ZC291ziC2Oh1zgxvLbpSkeU6snBXuw")