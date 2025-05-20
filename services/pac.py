# services/pac.py

import base64
import requests

def registrar_emisor_pac(rfc, cer_path, key_path, key_password, api_key):
    with open(cer_path, "rb") as cer_file:
        cer_b64 = base64.b64encode(cer_file.read()).decode()

    with open(key_path, "rb") as key_file:
        key_b64 = base64.b64encode(key_file.read()).decode()

    payload = {
        "rfc": rfc,
        "certificate": cer_b64,
        "key": key_b64,
        "password": key_password,
    }

    headers = {
        "Content-Type": "application/json",
        "x-api-key": api_key,
    }

    url = "https://sandbox-api.techbythree.com/api/v1/issuer"

    response = requests.post(url, json=payload, headers=headers)

    return response
