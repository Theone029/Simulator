# -*- coding: utf-8 -*-
import base64
import requests

def get_bearer():
    client_id = input("Client ID: ").strip()
    client_secret = input("Client Secret: ").strip()
    creds = f"{client_id}:{client_secret}".encode("ascii")
    b64_creds = base64.b64encode(creds).decode("ascii")

    headers = {
        "Authorization": f"Basic {b64_creds}",
        "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8"
    }

    resp = requests.post(
        "https://api.twitter.com/oauth2/token",
        headers=headers,
        data={"grant_type": "client_credentials"}
    )

    if resp.status_code == 200:
        token = resp.json().get("access_token")
        print(f"\n[✓] Bearer Token:\n\n{token}\n")
    else:
        print(f"\n[✗] Error: {resp.status_code} - {resp.text}")

if __name__ == "__main__":
    get_bearer()
