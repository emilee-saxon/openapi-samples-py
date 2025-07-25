import streamlit as st
import requests


# Global CSS style injection
st.markdown("""
<style>
/* --- General Link Style --- */
a.st-link {
color: #1f77b4;
text-decoration: none;
font-size: 16px;
font-weight: 500;
transition: all 0.2s ease;
}
a.st-link:hover {
text-decoration: underline;
color: #003057;
}

/* --- Button-style Link --- */
a.st-button-link {
display: inline-block;
padding: 10px 20px;
background-color: #003057;
color: white;
text-decoration: none;
border-radius: 6px;
font-weight: 600;
margin-top: 10px;
transition: background-color 0.3s ease;
}
a.st-button-link:hover {
background-color: #004e8c;
}

/* Optional: section title styling */
.section-title {
font-size: 20px;
font-weight: 600;
margin-top: 25px;
color: #003057;
border-bottom: 1px solid #ccc;
padding-bottom: 4px;
margin-bottom: 10px;
}
</style>
""", unsafe_allow_html=True)



st.title("Saxo Bank  Order Placement")

st.subheader("🔐 Authentication")
access_token = st.text_input("Access Token", type="password")
account_key = st.text_input("Account Key", type="password")

st.subheader("📝 Order Details")
uic = st.number_input("UIC", value=211)
asset_type = st.selectbox("Asset Type", ["Stock", "FxSpot", "Bond", "Option"])
order_type = st.selectbox("Order Type", ["Limit", "Market"])
buy_sell = st.selectbox("Buy/Sell", ["Buy", "Sell"])
order_price = st.text_input("Order Price", value="220")
amount = st.number_input("Amount", value=1)
duration_type = st.selectbox("Duration Type", ["DayOrder", "GoodTillCancel", "GoodTillDate"])
bid_price = st.number_input("Last Seen Client Bid Price", value=214.35)
ask_price = st.number_input("Last Seen Client Ask Price", value=214.41)
app_hint = st.number_input("App Hint", value=17039617)

# Live payload preview
payload = {
    "AccountKey": account_key,
    "Uic": uic,
    "AssetType": asset_type,
    "OrderType": order_type,
    "BuySell": buy_sell,
    "OrderPrice": order_price,
    "Amount": amount,
    "ManualOrder": True,
    "OrderDuration": {
        "DurationType": duration_type
    },
    "OrderRelation": "StandAlone",
    "OrderContext": {
        "LastSeenClientBidPrice": bid_price,
        "LastSeenClientAskPrice": ask_price
    },
    "AppHint": app_hint
}

# Show API endpoint
st.subheader("🔗 API Endpoint")
st.code("POST https://gateway.saxobank.com/sim/openapi/trade/v2/orders", language="http")


st.subheader("📦 Live Request Preview")
with st.expander("View JSON Payload", expanded=True):
    st.json(payload)


with open("orders/stockorders.py", "r") as file:
    code_body = file.read()




# Display with title and expandable section
with st.expander("🔐 Full Code Example", expanded=False):
    st.code(code_body, language="python", line_numbers=True)




# Optional: Add a button to send the request
if st.button("🚀 Place Order"):
    url = "https://gateway.saxobank.com/sim/openapi/trade/v2/orders"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    response = requests.post(url, json=payload, headers=headers)

    st.subheader("📬 Response")
    if response.status_code == 200:
        st.success("Order placed successfully!")
        st.json(response.json())
    else:
        st.error(f"Failed to place order: {response.status_code}")
        st.text(response.text)



