"""
Demo application of authenticating and making an authenticated request to the Formlabs Web API.

Get your Client ID and Secret at https://dashboard.formlabs.com/#developer
"""

import requests

CLIENT_ID = ""
CLIENT_SECRET = ""


def login_and_get_access_token():
    payload = {
        "grant_type": "client_credentials",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
    }
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
    }
    response = requests.request(
        "POST",
        "https://api.formlabs.com/developer/v1/o/token/",
        data=payload,
        headers=headers,
    )
    response.raise_for_status()
    access_token = response.json()["access_token"]
    return access_token


def request_all_printers_status(access_token):
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.request(
        "GET", "https://api.formlabs.com/developer/v1/printers/", headers=headers
    )
    response.raise_for_status()
    return response.json()


def output_printer_status(printers_status_json):
    print("Status of all printers:")
    for printer in printers_status_json:
        print(f"{printer['serial']}: {printer['printer_status']['status']}")


if __name__ == "__main__":
    if not CLIENT_ID or not CLIENT_SECRET:
        raise ValueError(
            "Please set CLIENT_ID and CLIENT_SECRET with your API client credentials"
        )
    access_token = login_and_get_access_token()
    status_data = request_all_printers_status(access_token)
    output_printer_status(status_data)
