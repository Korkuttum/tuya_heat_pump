import time
import hmac
import hashlib
import requests
import json

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

def main():
    print("Tuya Device Properties Fetcher")
    access_id = input("ACCESS_ID: ").strip()
    access_key = input("ACCESS_KEY: ").strip()
    api_endpoint_raw = input("API_ENDPOINT (e.g. eu, cn, us, in or full URL): ").strip()
    api_endpoint = resolve_api_endpoint(api_endpoint_raw)
    device_id = input("DEVICE_ID: ").strip()

    print("\nGetting token...")
    token = get_token(access_id, access_key, api_endpoint)
    print("Token received.")

    print("\nGetting properties for your device...")
    result = get_device_properties(access_id, access_key, api_endpoint, token, device_id)
    print(json.dumps(result, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()

    input("\nPress Enter to exit...")
    
