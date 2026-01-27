import tinytuya
import json
from getpass import getpass

def scan_tuya_devices():
    print("\n🔍 Scanning network for Tuya devices...\n")
    devices = tinytuya.deviceScan(verbose=False)

    if not devices:
        print("❌ No Tuya devices found on the network.")
        return None

    device_list = list(devices.items())

    print("Discovered devices:")
    print("-" * 60)

    for i, (ip, device) in enumerate(device_list, start=1):
        print(f"[{i}]")
        print(f"IP Address : {ip}")
        print(f"Device ID  : {device.get('gwId')}")
        print(f"Version    : {device.get('version')}")
        print(f"Product    : {device.get('productKey')}")
        print("-" * 60)

    return device_list

def select_device(device_list):
    while True:
        try:
            choice = int(input("Select device number to read DPS: "))
            if 1 <= choice <= len(device_list):
                return device_list[choice - 1]
            else:
                print("❌ Invalid selection.")
        except ValueError:
            print("❌ Please enter a valid number.")

def read_dps(ip, dev_id, version):
    print("\n🔑 Enter Local Key for selected device:")
    local_key = getpass("Local Key (hidden): ").strip()

    device = tinytuya.Device(
        dev_id=dev_id,
        address=ip,
        local_key=local_key,
        version=float(version)
    )

    print("\n📡 Reading DPS values...\n")
    data = device.status()

    print("Raw DPS Data:")
    print(json.dumps(data, indent=2, ensure_ascii=False))

    print("\nDPS Keys:")
    for key, value in data.get("dps", {}).items():
        print(f"DPS {key}: {value} (type: {type(value)})")

def wait_exit():
    input("\nPress ENTER to exit...")

def main():
    device_list = scan_tuya_devices()
    if not device_list:
        wait_exit()
        return

    ip, device = select_device(device_list)

    dev_id = device.get("gwId")
    version = device.get("version", 3.3)

    read_dps(ip, dev_id, version)

    wait_exit()

if __name__ == "__main__":
    main()
