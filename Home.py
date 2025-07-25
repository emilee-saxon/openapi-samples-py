import streamlit as st







# Custom banner
st.markdown("""
<div style="background-color:#003057;padding:20px 25px;border-radius:8px;margin-bottom:20px">
<h1 style="color:white;margin-bottom:0;"> Saxo OpenAPI Sample Dashboard</h1>
<p style="color:#dcdcdc;font-size:16px;margin-top:5px;">Explore Python-based examples for authentication, market data, and trading via Saxo Bank’s OpenAPI</p>
</div>
""", unsafe_allow_html=True)

# Table of Contents
st.markdown("##  Table of Contents")



st.page_link("pages/Authentication - Simple OAuth.py", label="Authentication", icon="🔒")



# Welcome section
st.subheader(" Welcome")
st.markdown("""
This dashboard is your entry point to a set of hands-on samples using the **Saxo Bank OpenAPI**.

Each section in the sidebar links to a dedicated page where you can:
-  Authenticate and decode OAuth2 tokens
-  Send basic API requests
-  Search instruments and view market metadata
-  Simulate trading operations (order placement)

All examples are written in Python and designed to work in **Saxo’s simulation environment** using a 24-hour access token.
""")

# Details section with anchors
st.markdown("---")
st.markdown("###  Authentication")
st.markdown("Decode your access token and inspect the claims using a JWT debugger.")

st.markdown("###  Basic API Requests")
st.markdown("Test connectivity and explore common OpenAPI endpoints interactively.")

st.markdown("###  Instrument Search")
st.markdown("Search for instruments using symbols and keywords, and browse metada-ta.")

st.markdown("###  Order Placement")
st.markdown("Simulate a market or limit order using a valid AccountKey and instrument UIC.")

# Optional: Link to Saxo Developer Portal
st.markdown("""
---
💡 Need a token? [Generate one on Saxo's Developer Portal](https://www.developer.saxo)
""")
