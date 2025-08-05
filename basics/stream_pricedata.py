import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import threading
import json
import websocket
import secrets
import time
from datetime import datetime
from collections import defaultdict
import requests

# Replace with your actual token
TOKEN = "eyJhbGciOiJFUzI1NiIsIng1dCI6IjczMEZDMUQwMUQ0MzM5Q0JGRTU3MTc0Q0NGREQ0RjExRDZENzgwNDYifQ.eyJvYWEiOiI3Nzc3MCIsImlzcyI6Im9hIiwiYWlkIjoiMTkzNyIsInVpZCI6IjZ2M3dHfElpQ0VBRk40NG5BY2kyR3c9PSIsImNpZCI6IjZ2M3dHfElpQ0VBRk40NG5BY2kyR3c9PSIsImlzYSI6IkZhbHNlIiwidGlkIjoiMzkxNyIsInNpZCI6ImQzM2JiMjUzNTExYTQ1Njk4ODczMTYzZDljMTE3NjVmIiwiZGdpIjoiODQiLCJleHAiOiIxNzU0MzgzNDkzIiwib2FsIjoiMUYiLCJpaWQiOiI0NjAxZWZiNzdiNDI0MjI1NjQ5MDA4ZGI5NTZkYjBlOCJ9.BPFG_TfX6Ci-gtFy577PQQrfelcD_gZ507Q70sdfZqo6ik_TfmBecPGYE6Cy-bXmAUfZ47zdHPded3ItiUpXsw"
CONTEXT_ID = secrets.token_urlsafe(10)
REF_ID = secrets.token_urlsafe(5)
quote_data = defaultdict(list)


def on_message(ws, message):
    
    index = 0

    try:
        # Parse message header
        msg_id = int.from_bytes(message[index:index + 8], byteorder="little")
        index += 8 + 2  # Skip version (2 bytes)

        # Reference ID
        ref_id_length = message[index]
        index += 1
        ref_id = message[index:index + ref_id_length].decode()
        index += ref_id_length
        # Payload format and size
        payload_format = message[index]
        index += 1
        payload_size = int.from_bytes(message[index:index + 4], byteorder="little")
        index += 4

        # Decode payload
        payload = message[index:index + payload_size].decode()
        index += payload_size

        # Parse and process quotes
        quotes = json.loads(payload)
        for quote in quotes:
            uic = quote.get('Uic')
            quote_info = quote.get('Quote', {})
            mid = quote_info.get('Mid')
            last_updated = quote.get('LastUpdated')

            if uic and mid and last_updated:
                try:
                    timestamp = datetime.strptime(last_updated, "%Y-%m-%dT%H:%M:%S.%fZ")
                    quote_data[uic].append({'timestamp': timestamp, 'mid': mid})
                    print(f"Quote for UIC {uic}: Mid={mid}, Time={timestamp}")
                except ValueError as ve:
                    print(f"Timestamp parsing error for UIC {uic}: {ve}")
            else:
                print(f"{quote}")

    except Exception as e:
        print(f"Error processing WebSocket message: {e}")


def on_error(ws, error):
    print(f"WebSocket error: {error}")

def on_close(ws, close_status_code, close_msg):
    print("WebSocket closed")

def on_open(ws):
    print("WebSocket opened, subscribing...")
    response = requests.post(
        "https://gateway.saxobank.com/openapi/trade/v1/infoprices/subscriptions",
        headers={"Authorization": "Bearer " + TOKEN},
        json={
            "Arguments": {"AssetType": "FxSpot", "Uics": "21,22,23,21700189"},
            "ContextId": CONTEXT_ID,
            "ReferenceId": REF_ID,
        },
    )
    if response.status_code == 201:
        print("Subscription successful")
    else:
        print("Subscription failed:", response.text)

def start_websocket():
    ws = websocket.WebSocketApp(
        f"wss://streaming.saxobank.com/openapi/streamingws/connect?ContextId={CONTEXT_ID}",
        header={"Authorization": f"Bearer {TOKEN}"},
        on_message=on_message,
        on_error=on_error,
        on_close=on_close,
        on_open=on_open,
    )
    ws.run_forever()

# Start WebSocket in background
ws_thread = threading.Thread(target=start_websocket)
ws_thread.daemon = True
ws_thread.start()

# Streamlit UI
st.set_page_config(page_title="Live Candlestick Chart", layout="wide")
st.title(" Live Candlestick Chart from Saxo Bank WebSocket")

selected_uic = st.selectbox("Select UIC", [21, 22, 23, 21700189])
placeholder = st.empty()



def convert_to_ohlc(data):
    df = pd.DataFrame(data)
    if df.empty:
        return pd.DataFrame()

    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df['mid'] = pd.to_numeric(df['mid'], errors='coerce')
    df.dropna(subset=['mid'], inplace=True)
    df.set_index('timestamp', inplace=True)

    ohlc = df['mid'].resample('5s').ohlc()
    return ohlc

# Live update loop
for _ in range(500):

    
    data = quote_data[selected_uic]
    ohlc_data = convert_to_ohlc(data)
    if not ohlc_data.empty:

        
        #go-candlestick viene da plotly
        fig = go.Figure(data=[go.Candlestick(
            x=ohlc_data.index,
            open=ohlc_data['open'],
            high=ohlc_data['high'],
            low=ohlc_data['low'],
            close=ohlc_data['close']
        )])
        
        fig.update_layout(
            title=f"UIC {selected_uic} Candlestick Chart",
            xaxis_title="Time",
            yaxis_title="Price",
            xaxis_rangeslider_visible=False
        )
        placeholder.plotly_chart(fig, use_container_width=True, key=f"chart_{selected_uic}_{time.time()}")
    time.sleep(1)
