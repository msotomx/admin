# services/pac.py

import base64
import requests

import requests
import base64

def registrar_emisor_pac(rfc, cer_path, key_path, password, api_token, client_id):
    url = f"https://dev.techbythree.com/api/v1/compatibilidad/{client_id}/RegistraEmisor"

    # Leer archivos y convertir a base64 si es requerido
    with open(cer_path, "rb") as f:
        certificado_b64 = base64.b64encode(f.read()).decode()

    with open(key_path, "rb") as f:
        llave_b64 = base64.b64encode(f.read()).decode()

    payload = {
        "rfc": rfc,
        "certificate": certificado_b64,
        "private_key": llave_b64,
        "private_key_password": password,
    }

    headers = {
        "Authorization": f"Bearer {api_token}",
        "X-CLIENT-ID": client_id,
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    response = requests.post(url, headers=headers, json=payload)
    
    return response

