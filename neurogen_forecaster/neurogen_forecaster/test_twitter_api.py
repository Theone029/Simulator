# -*- coding: utf-8 -*-
import requests, base64
import os
from dotenv import load_dotenv

load_dotenv()

client_id = os.getenv("TWITTER_CLIENT_ID")
client_secret = os.getenv("TWITTER_CLIENT_SECRET")

if not client_id or not client_secret:
    print("❌ Missing client credentials.")
    exit(1)

# Encode credentials
credentials = f"{client_id}:{client_secret}"
b64 = base64.b64encode(credentials.encode()).decode()

# Request bearer token
resp = requests.post(
    "https://api.twitter.com/oauth2/token",
    headers={"Authorization": f"Basic {b64}", "Content-Type": "application/x-www-form-urlencoded"},
    data={"grant_type": "client_credentials"}
)

if resp.status_code != 200:
    print(f"❌ Failed to fetch token: {resp.status_code} — {resp.text}")
    exit(1)

token = resp.json().get("access_token")
print("✅ Bearer token obtained.")

# Test basic search
test = requests.get(
    "https://api.twitter.com/1.1/search/tweets.json?q=neurogen&count=1",
    headers={"Authorization": f"Bearer {token}"}
)

if test.status_code != 200:
    print(f"❌ Token invalid or search failed: {test.status_code}")
else:
    print("✅ API call success. Twitter integration is viable.")
