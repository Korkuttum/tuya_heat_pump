# Tuya Heat Pump - Home Assistant Integration

<img src="https://www.arcelik.com.tr/media/resize/8510551100_MDM2_LOW_2.png/2000Wx2000H/image.webp" alt="Heat Pump" width="200"/>

 ⚠️ **Note:**  
> This integration has only been tested with the heat pump brands listed below.  
> If your heat pump is a different brand and the integration does not work, please run the script at the following link and share the generated file with me:  
> [tuya_api_test.py](https://github.com/Korkuttum/tuya_heat_pump/blob/7d4303902f08a66663448902a00e3fc71efc0f4b/test/tuya_api_test.py)
### Supported Brands
- Arçelik
---

This project allows you to control and monitor your Tuya cloud-based heat pump device through Home Assistant.

---

## Prerequisites

### Enabling Tuya IoT Cloud Service

To use this integration, you need to create a project in the Tuya IoT Platform, grant API access, and link your device to the project.

**Steps:**

1. Log in to [Tuya IoT Platform](https://iot.tuya.com/).
2. Go to “Cloud > Project Management” and create a new project or select an existing one.
3. In project details, go to the “API Group Authorization” tab.
4. Authorize essential API groups such as “Device Status” and “Device Control”.
5. In the “Link Device” section, add your heat pump device to the project.
6. Retrieve your Access ID and Access Secret from the project panel.

> ⚠️ **Important:** The integration will not work without API authorization and device linking.

---

## Installation

[![Open your Home Assistant instance and open a repository inside the Home Assistant Community Store](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=Korkuttum&repository=tuya_heat_pump&category=integration)

### Method 1: Installation via HACS (Recommended)

1. Make sure you have HACS installed in your Home Assistant instance.
2. Click on HACS in the sidebar.
3. Click the three dots in the top right corner and select “Custom Repositories”.
4. Add the following repository URL and select “Integration” as the category:  
   ```
   https://github.com/Korkuttum/tuya_heat_pump
   ```
5. Click “ADD”.
6. Find "Tuya Heat Pump" in the integrations list and install it.
7. Restart Home Assistant.

Or, you can add it directly using the HACS badge above.

### Method 2: Manual Installation

- Upload all files to  
  `custom_components/tuya_heat_pump` folder inside your Home Assistant configuration directory.
- Restart Home Assistant.

---

## Configuration

After installation, restart Home Assistant and follow these steps:

1. Go to “Settings > Devices & Services”.
2. Click “Add Integration”.
3. Search for and select “Tuya Heat Pump”.
4. Enter your Tuya IoT Platform credentials:
    - Access ID
    - Access Secret
    - Device ID

---

## Notes

- You can monitor and control features like temperature, operation mode, and fan speed.
- Easily use in automations and dashboards.

---

## Support My Work

If you find this integration helpful, consider supporting the development:

[![Become a Patreon](https://img.shields.io/badge/Become_a-Patron-red.svg?style=for-the-badge&logo=patreon)](https://www.patreon.com/korkuttum)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Disclaimer

This integration is an independent project and is not affiliated with, endorsed by, or connected to Tuya Inc. in any way. This is a community project provided "as is" without warranty of any kind. Use at your own risk.
