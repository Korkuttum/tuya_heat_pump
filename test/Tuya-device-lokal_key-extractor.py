import time
import hmac
import hashlib
import requests
import json

def resolve_api_endpoint(region_input):
    region_map = {
        "cn": "https://openapi.tuyacn.com",
        "us": "https://openapi.tuyaus.com",
        "eu": "https://openapi.tuyaeu.com",
        "in": "https://openapi.tuyain.com",
    }
    region_input = region_input.strip().lower()
    return region_map.get(region_input, region_input)

def sign_request(access_id, access_key, method, path, t, token=None, body=""):
    content_sha256 = hashlib.sha256(body.encode('utf-8')).hexdigest()
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
        "sign_method": "HMAC-SHA256",
        "Content-Type": "application/json"
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    data = response.json()
    if not data.get("success"):
        raise ValueError(f"Token request failed: {data.get('msg', data)}")
    return data["result"]["access_token"]

def get_device_info(access_id, access_key, api_endpoint, token, device_id):
    path = f"/v1.0/devices/{device_id}"
    url = f"{api_endpoint}{path}"
    t = str(int(time.time() * 1000))
    sign = sign_request(access_id, access_key, "GET", path, t, token)
    headers = {
        "client_id": access_id,
        "sign": sign,
        "t": t,
        "sign_method": "HMAC-SHA256",
        "access_token": token,
        "Content-Type": "application/json",
        "mode": "cors"
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    data = response.json()
    if not data.get("success"):
        raise ValueError(f"Device query failed: {data.get('msg', data)}")
    return data.get("result", {})

def main():
    print("Tuya Device Local Key Extractor")
    print("-------------------------------")
    print("")

    access_id  = input("Client ID / Access ID      : ").strip()
    access_key = input("Client Secret / Access Key : ").strip()
    region_raw = input("Region (eu/cn/us/in) [eu]  : ").strip() or "eu"
    device_id  = input("Device ID                  : ").strip()

    api_endpoint = resolve_api_endpoint(region_raw)
    print("")
    print("Using endpoint:", api_endpoint)
    print("")

    try:
        print("Obtaining token...")
        token = get_token(access_id, access_key, api_endpoint)
        print("Token obtained.")

        print("Retrieving device information...")
        device_info = get_device_info(access_id, access_key, api_endpoint, token, device_id)

        local_key = device_info.get("local_key", "").strip()
        device_name = device_info.get('name', '—')

        print("")
        print("----------------------------------------")
        print("Device ID     :", device_id)
        print("Device Name   :", device_name)
        print("Local Key     :", local_key if local_key else "(empty / hidden by Tuya)")
        print("----------------------------------------")

        if not local_key:
            print("")
            print("Local Key Note:")
            print("  Tuya hides local_key on most non-gateway devices (since ~2022 for security).")
            print("  It usually only appears for gateways/hubs.")
            print("  Alternatives:")
            print("    - python -m tinytuya wizard")
            print("    - Home Assistant + LocalTuya integration")
            print("    - Extract from Smart Life app database (emulator + old version)")

    except Exception as e:
        print("")
        print("Error:", str(e))
        if 'response' in locals() and hasattr(response, 'text'):
            try:
                print("Server response:")
                print(json.dumps(response.json(), indent=2))
            except:
                print(response.text)

    print("")
    input("Press Enter to exit...")

if __name__ == "__main__":
    main()
