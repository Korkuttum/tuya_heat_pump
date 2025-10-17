import time
import hmac
import hashlib
import requests
import json
import os
from datetime import datetime

def resolve_api_endpoint(endpoint_input):
    region_map = {
        "cn": "https://openapi.tuyacn.com",
        "us": "https://openapi.tuyaus.com", 
        "eu": "https://openapi.tuyaeu.com",
        "in": "https://openapi.tuyain.com"
    }
    endpoint_input = endpoint_input.strip().lower()
    return region_map.get(endpoint_input, endpoint_input)

def sign_request(access_id, access_key, method, path, t, token=None, body=""):
    content_sha256 = hashlib.sha256(body.encode('utf8')).hexdigest()
    string_to_sign = f"{method}\n{content_sha256}\n\n{path}"
    message = access_id + (token or "") + t + string_to_sign
    signature = hmac.new(
        access_key.encode("utf-8"),
        message.encode("utf-8"), 
        hashlib.sha256
    ).hexdigest().upper()
    return signature

def get_token(access_id, access_key, api_endpoint):
    path = "/v1.0/token?grant_type=1"
    url = f"{api_endpoint}{path}"
    t = str(int(time.time() * 1000))
    sign = sign_request(access_id, access_key, "GET", path, t)
    headers = {
        "client_id": access_id,
        "sign": sign,
        "t": t,
        "sign_method": "HMAC-SHA256"
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    result = response.json()
    return result["result"]["access_token"]

def get_device_properties(access_id, access_key, api_endpoint, token, device_id):
    path = f"/v2.0/cloud/thing/{device_id}/shadow/properties"
    url = f"{api_endpoint}{path}"
    t = str(int(time.time() * 1000))
    sign = sign_request(access_id, access_key, "GET", path, t, token)
    headers = {
        "client_id": access_id,
        "sign": sign,
        "t": t,
        "sign_method": "HMAC-SHA256",
        "mode": "cors",
        "Content-Type": "application/json",
        "access_token": token
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()

def get_device_model(access_id, access_key, api_endpoint, token, device_id):
    path = f"/v2.0/cloud/thing/{device_id}/model"
    url = f"{api_endpoint}{path}"
    t = str(int(time.time() * 1000))
    sign = sign_request(access_id, access_key, "GET", path, t, token)
    headers = {
        "client_id": access_id,
        "sign": sign,
        "t": t,
        "sign_method": "HMAC-SHA256",
        "mode": "cors", 
        "Content-Type": "application/json",
        "access_token": token
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()

def save_to_txt(data, filename):
    """Veriyi txt dosyasına kaydet"""
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(data)
    return filename

def main():
    print("Tuya Device Properties & Model Fetcher")
    print("=" * 50)
    
    access_id = input("ACCESS_ID: ").strip()
    access_key = input("ACCESS_KEY: ").strip()
    api_endpoint_raw = input("API_ENDPOINT (e.g. eu, cn, us, in or full URL): ").strip()
    api_endpoint = resolve_api_endpoint(api_endpoint_raw)
    device_id = input("DEVICE_ID: ").strip()

    print("\nGetting token...")
    token = get_token(access_id, access_key, api_endpoint)
    print("✓ Token received.")

    print("\nGetting properties for your device...")
    properties = get_device_properties(access_id, access_key, api_endpoint, token, device_id)
    print("✓ Properties received.")

    print("Getting device model...")
    model = get_device_model(access_id, access_key, api_endpoint, token, device_id)
    print("✓ Model received.")

    # Tüm veriyi birleştir
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"tuya_device_data_{timestamp}.txt"
    
    output_data = f"""TUYA DEVICE DATA
Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
Device ID: {device_id}
API Endpoint: {api_endpoint}

=== DEVICE PROPERTIES ===
{json.dumps(properties, indent=2, ensure_ascii=False)}

=== DEVICE MODEL ===
{json.dumps(model, indent=2, ensure_ascii=False)}
"""

    # Model datayı parse etmeye çalış
    try:
        model_json = json.loads(model["result"]["model"])
        output_data += f"""

=== PARSED MODEL DATA ===
{json.dumps(model_json, indent=2, ensure_ascii=False)}
"""
    except Exception as e:
        output_data += f"""

=== RAW MODEL DATA ===
{model["result"]["model"]}

Parse Error: {e}
"""

    # Ekrana da göster
    print("\n" + "=" * 50)
    print("RESULTS:")
    print("=" * 50)
    
    # Sadece özet göster
    if 'result' in properties and 'properties' in properties['result']:
        print(f"Found {len(properties['result']['properties'])} properties:")
        for prop in properties['result']['properties']:
            print(f"  - {prop['code']}: {prop.get('value', 'N/A')}")
    
    # Dosyaya kaydet
    filepath = save_to_txt(output_data, filename)
    print(f"\n✓ All data saved to: {filepath}")
    print("✓ You can send this file to the developer.")
    
    # Pencereyi açık tut
    print("\n" + "=" * 50)
    input("Press ENTER to exit...")

if __name__ == "__main__":
    main()
