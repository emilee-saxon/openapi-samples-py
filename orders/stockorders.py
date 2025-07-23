import requests

# Replace with your actual access token and account key
access_token = "eyJhbGciOiJFUzI1NiIsIng1dCI6IjI3RTlCOTAzRUNGMjExMDlBREU1RTVCOUVDMDgxNkI2QjQ5REEwRkEifQ.eyJvYWEiOiI3Nzc3MCIsImlzcyI6Im9hIiwiYWlkIjoiNjYwOSIsInVpZCI6IjBZakxGMVktSktjU3NOVGhSekVFVEE9PSIsImNpZCI6IjBZakxGMVktSktjU3NOVGhSekVFVEE9PSIsImlzYSI6IkZhbHNlIiwidGlkIjoiMTE2MzYiLCJzaWQiOiI0OThjYTNkNWMyMTQ0ODY4OTRjNmMxNjMwMWQ0MDBmYyIsImRnaSI6Ijg0IiwiZXhwIjoiMTc1MzI3NjE1NCIsIm9hbCI6IjFGIiwiaWlkIjoiZWZmMzVlNzMxYWU4NDBmNTljZDAwOGRkNzEwMDk5NDAifQ.tVehMZSXqnqip7gHCVXnf-cV5VZK0uBfwMjODRilV-7S15_5gnog34ge6XtOIvkD3B4iZm9kZ0Y8thFmgSAmRQ"
account_key = "0YjLF1Y-JKcSsNThRzEETA=="


# API endpoint
url = "https://gateway.saxobank.com/sim/openapi/trade/v2/orders"

# Headers
headers = {
    "Authorization": f"Bearer {access_token}",
    "Content-Type": "application/json"
}

# Order payload for a LIMIT
payload = {
    "AccountKey": account_key,
    "Uic": 211,
    "AssetType": "Stock",
    "OrderType": "Limit",
    "BuySell": "Buy",
    "OrderPrice": "220",
    "Amount": 1,
    "ManualOrder": True,
    "OrderDuration": {
        "DurationType": "DayOrder"
    },
    "OrderRelation": "StandAlone",
    "OrderContext": {
        "LastSeenClientBidPrice": 214.35,
        "LastSeenClientAskPrice": 214.41
    },
    "AppHint": 17039617
}

# Send the POST request
response = requests.post(url, json=payload, headers=headers)

# Handle the response
if response.status_code == 200:
    print("Order placed successfully!")
    print(response.json())
else:
    print("Failed to place order:")
    print(response.status_code, response.text)
