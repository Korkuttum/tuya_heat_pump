# Tuya Heat Pump for Home Assistant

<p align="center">
  <img src="https://raw.githubusercontent.com/Korkuttum/tuya_heat_pump/main/images/heatpump.webp" alt="Tuya Heat Pump" width="200">
</p>

A custom Home Assistant integration for monitoring and controlling supported Tuya-based heat pumps through the Tuya Cloud API or directly over the local network.

[![Open in HACS](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=Korkuttum&repository=tuya_heat_pump&category=integration)

> [!IMPORTANT]
> Compatibility depends on the Tuya **Model ID** and datapoint definitions, not only on the brand printed on the heat pump. Rebranded units may share the same controller and model mapping, while two units from the same brand may use different datapoints.

## Features

- Cloud connection through the Tuya IoT Platform
- Local LAN connection through TinyTuya
- Optional MQTT push updates through the Tuya Smart or Smart Life app
- Per-model mappings for sensors and controls
- Automatic fallback to the default mapping when a Model ID is unknown
- Home Assistant entities for:
  - sensors and binary sensors
  - switches
  - numeric settings
  - selectable operating modes
  - text settings, when exposed by the device
- Cloud commands and local control
- Configurable cloud polling interval
- Automatic return to polling if MQTT is unavailable or incomplete

The exact entities available depend on the model mapping and the datapoints exposed by your device.

## Compatibility

See the [detailed supported-model list](supported_models.md) for tested brands, models, Tuya Model IDs, and the related issue or pull request.

An unlisted heat pump may still work if it uses the same Tuya Model ID and datapoint layout as a supported device. If no matching model file exists, the integration loads the generic `default` mapping. A successful installation therefore does not necessarily mean that every entity is correctly mapped.

If your device is not listed or produces missing, unavailable, or incorrect entities, follow [Adding support for a new model](#adding-support-for-a-new-model).

## Requirements

- Home Assistant 2023.1.0 or newer
- A Tuya Smart or Smart Life account with the heat pump already paired
- A Tuya IoT Platform Cloud project linked to that app account
- The following Tuya project values:
  - Access ID
  - Access Secret (shown as **Access Key** in the integration)
  - Device ID
  - correct data-center region
- For local mode:
  - device IP address
  - Local Key
  - Tuya protocol version: 3.1, 3.3, 3.4, or 3.5
  - Home Assistant and the heat pump on the same local network

> [!NOTE]
> The setup form currently requests the Tuya Cloud credentials for both connection modes. In local mode, they are used to retrieve device information and select the correct model mapping; normal status updates and commands then use the LAN connection.

## Configure the Tuya IoT Platform

1. Sign in to the [Tuya IoT Platform](https://iot.tuya.com/).
2. Open **Cloud > Development** or **Cloud > Project Management**, then create or select a Cloud project.
3. Use the data center that matches the region of your Tuya Smart or Smart Life account.
4. Open the project's **Devices** section.
5. If the heat pump is not listed, open **Link Tuya App Account**, add an app account, and scan the displayed QR code with the mobile app.
6. In **Service API**, authorize:
   - IoT Core
   - Smart Home Basic Service
   - Device Status Notification
   - Authorization Token Management
7. Copy the project's **Access ID** and **Access Secret**.
8. Copy the heat pump's **Device ID** from the device list.

If token creation or device discovery fails, first verify the selected region, API authorizations, and app-account link.

## Installation

### HACS

1. Install [HACS](https://www.hacs.xyz/) if it is not already available.
2. Open the button below or add this repository as a custom integration repository.
3. Download **Tuya Heat Pump**.
4. Restart Home Assistant.

[![Open in HACS](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=Korkuttum&repository=tuya_heat_pump&category=integration)

### Manual installation

1. Download the latest repository release.
2. Copy `custom_components/tuya_heat_pump` into your Home Assistant `custom_components` directory.
3. Restart Home Assistant.

The resulting path must be:

```text
<config>/custom_components/tuya_heat_pump/manifest.json
```

## Configuration

In Home Assistant:

1. Open **Settings > Devices & services**.
2. Select **Add integration**.
3. Search for **Tuya Heat Pump**.
4. Enter the Access ID, Access Key, Device ID, and region.
5. Select a connection type.
6. Complete the fields for the selected mode.

### Connection modes

| Mode | Data path | Additional values | Update behavior | Main trade-off |
| --- | --- | --- | --- | --- |
| Cloud | Tuya IoT API | None beyond the common Cloud credentials | Polling, 3 minutes by default | Works remotely but depends on Tuya Cloud and API availability |
| Local | Direct LAN connection | IP, Local Key, protocol version | Local status/push handling | Fast and avoids Cloud API limits for normal operation, but requires LAN reachability and valid local credentials |
| Cloud + MQTT | Tuya IoT API plus Tuya app sharing | Optional User Code and QR approval | Push when coverage is sufficient; polling remains as fallback | Update coverage varies by device and Tuya's standard instruction set |

The cloud polling interval can be changed from the integration options between 1 and 60 minutes.

### Optional MQTT updates

MQTT support is optional and only offered during Cloud setup.

1. In the Tuya Smart or Smart Life app, open **Me > Settings > Account and Security > User Code**.
2. Enter that User Code in the integration setup form.
3. Scan the Home Assistant QR code from the Tuya app using **+ > Scan**.
4. Return to Home Assistant and submit the form.

If MQTT exposes every datapoint required by the selected model, regular polling is paused while MQTT remains healthy. If coverage is incomplete, MQTT only triggers an immediate refresh and polling continues. If the MQTT connection drops, the integration automatically restores polling.

Leave the User Code blank to use standard polling without MQTT.

## Adding support for a new model

Use the diagnostic script when your heat pump is not listed or its entities are incorrectly mapped:

[`test/tuya_api_test.py`](test/tuya_api_test.py)

The script:

1. requests your Access ID, Access Key, API region, and Device ID;
2. obtains a temporary Tuya Cloud token;
3. reads the device shadow properties;
4. reads the Tuya device model definition;
5. writes the result to a timestamped `tuya_device_data_*.txt` file.

Run it on a computer with Python 3 and the `requests` package:

```bash
python3 -m pip install requests
python3 test/tuya_api_test.py
```

Review the generated file before attaching it to a [new GitHub issue](https://github.com/Korkuttum/tuya_heat_pump/issues/new). Include the heat-pump brand and exact commercial model.

> [!CAUTION]
> Never publish your Access ID, Access Secret/Key, Local Key, access token, or Tuya account credentials. The script does not intentionally write the Access Key or token to its output file, but the report does contain the Device ID, current property values, and the complete device model definition. Redact anything you do not want to share.

## Troubleshooting

### Authentication failed

Check that:

- Access ID and Access Key belong to the same Tuya Cloud project;
- the selected region matches the app account's data center;
- the required Service APIs are authorized;
- the app account is still linked to the Cloud project;
- the Device ID belongs to that linked account.

### Local connection failed

Check that:

- the device IP has not changed;
- Home Assistant can reach that IP;
- the Local Key is current;
- the selected protocol version matches the device;
- VLAN and firewall rules allow traffic between Home Assistant and the heat pump.

Re-pairing or removing a Tuya device can change its Local Key.

### Setup succeeds but entities are missing

This usually indicates an unknown Model ID or a datapoint mismatch. Compare the device Model ID with [supported_models.md](supported_models.md), then generate a diagnostic report as described above.

### MQTT does not provide every update

This can be normal. Tuya may expose only part of a device through its standard instruction set. The integration keeps polling whenever MQTT coverage is insufficient, so control and monitoring continue without relying exclusively on push events.

## Support

For bugs and model-support requests, use the [GitHub issue tracker](https://github.com/Korkuttum/tuya_heat_pump/issues).

If you find this integration useful, you can support its development:

[![Become a Patreon](https://img.shields.io/badge/Become_a-Patron-red.svg?style=for-the-badge&logo=patreon)](https://www.patreon.com/korkuttum)

## License

This project is licensed under the [MIT License](LICENSE).

## Disclaimer

This is an independent community project and is not affiliated with, endorsed by, or connected to Tuya Inc. It is provided as-is, without warranty. Use it at your own risk.
