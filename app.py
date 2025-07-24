import streamlit as st
import requests
import json

# Create Streamlit components to simulate the required JavaScript elements
def streamlit_app():
    
    st.title("Order Type Modifier ")

    # Placeholder for order object
    order_object_json = '{"OrderType": "Limit", "OrderDuration": {"DurationType": "DAY"}, "AssetType": "FxSpot", "Uic": 1234}'
    new_order_object = json.loads(order_object_json)

    # Order type selection
    order_type = st.selectbox(
        "Select Order Type",
        ["Limit", "StopLimit", "TrailingStop", "TrailingStopIfBid", 
         "TrailingStopIfOffered", "TrailingStopIfTraded", "TriggerBreakout", 
         "TriggerLimit", "TriggerStop"]
    )
    
    # Input for bearer token and fictive price (similar logic as in JS)
    bearer_token = st.text_input("Enter Bearer Token")
    fictive_price = st.number_input("Fictive Price", value=1.0)

    def change_order_type():
        new_order_object['OrderType'] = order_type
        new_order_object.pop('OrderPrice', None)
        new_order_object.pop('StopLimitPrice', None)
        new_order_object.pop('TrailingstopDistanceToMarket', None)
        new_order_object.pop('TrailingStopStep', None)

        if new_order_object['OrderType'] == "Limit":
            # Simulate fetching data from an API
            response = requests.get(
                f'YOUR_API_URL/trade/v1/infoprices?AssetType={new_order_object["AssetType"]}&uic={new_order_object["Uic"]}&FieldGroups=DisplayAndFormat,Quote',
                headers={
                    "Authorization": f"Bearer {bearer_token}"
                }
            )

            if response.ok:
                response_json = response.json()
                if response_json.get('Quote', {}).get('PriceTypeBid', '') == "NoAccess":
                    new_order_object['OrderPrice'] = fictive_price

        elif new_order_object['OrderType'] == "StopLimit":
            new_order_object['OrderPrice'] = fictive_price
            new_order_object['StopLimitPrice'] = fictive_price + 1

        elif new_order_object['OrderType'] in ["TrailingStop", "TrailingStopIfBid", 
                                               "TrailingStopIfOffered", "TrailingStopIfTraded"]:
            new_order_object['OrderPrice'] = fictive_price
            new_order_object['TrailingstopDistanceToMarket'] = 1
            new_order_object['TrailingStopStep'] = 0.1

        else:
            st.error("Unsupported order type")

        st.json(new_order_object)

    st.button("Change Order Type", on_click=change_order_type)

streamlit_app()