# Tuya Heat Pump - Home Assistant Integration

<img src="https://raw.githubusercontent.com/Korkuttum/tuya_heat_pump/main-2.2.0/images/heatpump.webp" width="200">

 ⚠️ **Note:**  
> This integration has only been tested with the heat pump brands listed below.  
> If your heat pump is a different brand and the integration does not work, please run the script at the following link and share the generated file with me:  
> [tuya_api_test.py](https://github.com/Korkuttum/tuya_heat_pump/blob/7d4303902f08a66663448902a00e3fc71efc0f4b/test/tuya_api_test.py)

<details>
 
<summary><b>Supported Heat Pump Models (31 Models)</b></summary>

|  | Brand / Model | GitHub User | Model File | Issue/PR | Published |
|---|---------------|-------------|------------|----------|-----------|
| 1 | Arçelik (Beko, Grundig) | [@korkuttum](https://github.com/korkuttum) | [000004wtcv](https://github.com/Korkuttum/tuya_heat_pump/blob/main-2.3.0/custom_components/tuya_heat_pump/models/000004wtcv.py) | — | * |
| 2 | Adlar Castra | [@rznq0q](https://github.com/rznq0q) | [000004u5nz](https://github.com/Korkuttum/tuya_heat_pump/blob/main-2.3.0/custom_components/tuya_heat_pump/models/000004u5nz.py) | [#4](https://github.com/Korkuttum/tuya_heat_pump/issues/4) | * |
| 3 | Aquark| [@reitermarkus](https://github.com/reitermarkus) | [000000324z](https://github.com/Korkuttum/tuya_heat_pump/blob/main-2.3.0/custom_components/tuya_heat_pump/models/000000324z.py) | [#29](https://github.com/Korkuttum/tuya_heat_pump/issues/29) | * |
| 4 | Aquastrong| [@lmatter](https://github.com/lmatter) | [e1k1k2nw](https://github.com/Korkuttum/tuya_heat_pump/blob/main-2.3.0/custom_components/tuya_heat_pump/models/e1k1k2nw.py) | [#50](https://github.com/Korkuttum/tuya_heat_pump/pull/50) | * |
| 5 | Aquatech X6 | [@dabanhfreak](https://github.com/dabanhfreak) | [elrnos](https://github.com/Korkuttum/tuya_heat_pump/blob/main-2.3.0/custom_components/tuya_heat_pump/models/elrnos.py) | [#10](https://github.com/Korkuttum/tuya_heat_pump/issues/10) | * |
| 6 | Cordivari Vestalis | [@carpenv](https://github.com/carpenv) | [eu20ns](https://github.com/Korkuttum/tuya_heat_pump/blob/main-2.3.0/custom_components/tuya_heat_pump/models/eu20ns.py) | [#9](https://github.com/Korkuttum/tuya_heat_pump/issues/9) | * |
| 7 | Della | [@Chrissica06](https://github.com/Chrissica06) | [e1moeap8](https://github.com/Korkuttum/tuya_heat_pump/blob/main-2.3.0/custom_components/tuya_heat_pump/models/e1moeap8.py) | [#54](https://github.com/Korkuttum/tuya_heat_pump/issues/54) | * |
| 8 | Ecologic Ecopool | [@danilofborges](https://github.com/danilofborges) | [e8d6pg](https://github.com/Korkuttum/tuya_heat_pump/blob/main-2.3.0/custom_components/tuya_heat_pump/models/e8d6pg.py) | [#24](https://github.com/Korkuttum/tuya_heat_pump/issues/24) | * |
| 9 | EnviroSun HP+ (Still not working yet.) | [@jascham](https://github.com/jascham) | [e1mnja6s](https://github.com/Korkuttum/tuya_heat_pump/blob/main-2.3.0/custom_components/tuya_heat_pump/models/e1mnja6s.py) | [#8](https://github.com/Korkuttum/tuya_heat_pump/issues/8) | * |
| 10 | Evoheat 40T | [@andrewboller](https://github.com/andrewboller) | [000004joyp](https://github.com/Korkuttum/tuya_heat_pump/blob/main-2.3.0/custom_components/tuya_heat_pump/models/000004joyp.py) | [#12](https://github.com/Korkuttum/tuya_heat_pump/issues/12) | * |
| 11 | Fairland | [@bradleewright](https://github.com/bradleewright) | [000004jrci](https://github.com/Korkuttum/tuya_heat_pump/blob/main-2.3.0/custom_components/tuya_heat_pump/models/000004jrci.py) | [#40](https://github.com/Korkuttum/tuya_heat_pump/issues/40) | * |
| 12 | Fairland Inverter Plus | [@latecka](https://github.com/latecka) | [0000000tqc](https://github.com/Korkuttum/tuya_heat_pump/blob/main-2.3.0/custom_components/tuya_heat_pump/models/0000000tqc.py) | [#55](https://github.com/Korkuttum/tuya_heat_pump/issues/55) | * |
| 13 | Heative Next | [@Franksb](https://github.com/Franksb) | [e1kcc5hw](https://github.com/Korkuttum/tuya_heat_pump/blob/main-2.3.0/custom_components/tuya_heat_pump/models/e1kcc5hw.py) | [#6](https://github.com/Korkuttum/tuya_heat_pump/issues/6) | * |
| 14 | Inventor Xforce | [@DrRikons](https://github.com/DrRikons) | [000004lh21](https://github.com/Korkuttum/tuya_heat_pump/blob/main-2.3.0/custom_components/tuya_heat_pump/models/000004lh21.py) | [#21](https://github.com/Korkuttum/tuya_heat_pump/issues/21) | * |
| 15 | IPS Pool Systems | [@KaaNee](https://github.com/KaaNee) | [000004joyp](https://github.com/Korkuttum/tuya_heat_pump/blob/main-2.3.0/custom_components/tuya_heat_pump/models/000004joyp.py) | [#48](https://github.com/Korkuttum/tuya_heat_pump/issues/48) | * |
| 16 | ITS | [@Bladeclaw](https://github.com/Bladeclaw) | [000004stwy](https://github.com/Korkuttum/tuya_heat_pump/blob/main-2.3.0/custom_components/tuya_heat_pump/models/000004stwy.py) | [#57](https://github.com/Korkuttum/tuya_heat_pump/issues/57) |  |
| 17 | Ivapool | [@fehrudi87](https://github.com/fehrudi87) | [000004kb7r](https://github.com/Korkuttum/tuya_heat_pump/blob/main-2.3.0/custom_components/tuya_heat_pump/models/000004kb7r.py) | [#43](https://github.com/Korkuttum/tuya_heat_pump/issues/43) | * |
| 18 | Kensol | [@VaporX25](https://github.com/VaporX25) | [fdru4s](https://github.com/Korkuttum/tuya_heat_pump/blob/main-2.3.0/custom_components/tuya_heat_pump/models/fdru4s.py) | [#56](https://github.com/Korkuttum/tuya_heat_pump/issues/56) | * |
| 19 | Kushiro (Luqstoff) | [@tortu091](https://github.com/tortu091) | [0000038m77](https://github.com/Korkuttum/tuya_heat_pump/blob/main-2.3.0/custom_components/tuya_heat_pump/models/0000038m77.py) | [#11](https://github.com/Korkuttum/tuya_heat_pump/pull/11) | * |
| 20 | Mitte Aerotermia | [@jeroen-s](https://github.com/jeroen-s) | [e1kcc5hw](https://github.com/Korkuttum/tuya_heat_pump/blob/main-2.3.0/custom_components/tuya_heat_pump/models/e1kcc5hw.py) | [#22](https://github.com/Korkuttum/tuya_heat_pump/issues/22) | * |
| 21 | MyCond BeeThermic | [@RuslanNovak](https://github.com/RuslanNovak) | [000003ynwv](https://github.com/Korkuttum/tuya_heat_pump/blob/main-2.3.0/custom_components/tuya_heat_pump/models/000003ynwv.py) | [#7](https://github.com/Korkuttum/tuya_heat_pump/issues/7) | * |
| 22 | Poolsana | [@rommelfs](https://github.com/rommelfs) | [e1kd83ng](https://github.com/Korkuttum/tuya_heat_pump/blob/main-2.3.0/custom_components/tuya_heat_pump/models/e1kd83ng.py) | [#16](https://github.com/Korkuttum/tuya_heat_pump/issues/16) | * |
| 23 | Power World | [@brownnath2000](https://github.com/brownnath2000) | [fc1fls](https://github.com/Korkuttum/tuya_heat_pump/blob/main-2.3.0/custom_components/tuya_heat_pump/models/fc1fls.py) | [#26](https://github.com/Korkuttum/tuya_heat_pump/issues/26) | * |
| 24 | Power World PW030 | [@HeideggerDaniel](https://github.com/HeideggerDaniel) | [000004jong](https://github.com/Korkuttum/tuya_heat_pump/blob/main-2.3.0/custom_components/tuya_heat_pump/models/000004jong.py) | [#44](https://github.com/Korkuttum/tuya_heat_pump/issues/44) | * |
| 25 | Power World R290 Full DC | [@tomoo777](https://github.com/tomoo777) | [e1k5wjuc](https://github.com/Korkuttum/tuya_heat_pump/blob/main-2.3.0/custom_components/tuya_heat_pump/models/e1k5wjuc.py) | [#53](https://github.com/Korkuttum/tuya_heat_pump/issues/53) | * |
| 26 | Pure Blue Onyx | [@warrenjmcdonald](https://github.com/warrenjmcdonald) | [f6ry00](https://github.com/Korkuttum/tuya_heat_pump/blob/main-2.3.0/custom_components/tuya_heat_pump/models/f6ry00.py) | [#20](https://github.com/Korkuttum/tuya_heat_pump/issues/20) | * |
| 27 | SolarEast | [@Harm1990](https://github.com/Harm1990) | [e1kt5k90](https://github.com/Korkuttum/tuya_heat_pump/blob/main-2.3.0/custom_components/tuya_heat_pump/models/e1kt5k90.py) | [#32](https://github.com/Korkuttum/tuya_heat_pump/issues/32) | * |
| 28 | Water TechniX | [@SabreT1952](https://github.com/SabreT1952) | [000003jtyb](https://github.com/Korkuttum/tuya_heat_pump/blob/main-2.3.0/custom_components/tuya_heat_pump/models/000003jtyb.py) | [#5](https://github.com/Korkuttum/tuya_heat_pump/issues/5) | * |
| 29 | W'eau | [@rznq0q](https://github.com/rznq0q) | [e1kvebno](https://github.com/Korkuttum/tuya_heat_pump/blob/main-2.3.0/custom_components/tuya_heat_pump/models/e1kvebno.py) | [#27](https://github.com/Korkuttum/tuya_heat_pump/issues/27) | * |
| 30 | W'eau WFI-007 | [@OdynBrouwer](https://github.com/OdynBrouwer) | [000003p0fy](https://github.com/Korkuttum/tuya_heat_pump/blob/main-2.3.0/custom_components/tuya_heat_pump/models/000003p0fy.py) | [#39](https://github.com/Korkuttum/tuya_heat_pump/issues/39) | * |
| 31 | Wopoltop | [@goofee76](https://github.com/goofee76) | [enhs6o](https://github.com/Korkuttum/tuya_heat_pump/blob/main-2.3.0/custom_components/tuya_heat_pump/models/enhs6o.py) | [#42](https://github.com/Korkuttum/tuya_heat_pump/issues/42) | * |

</details>

> Model files have been prepared based on user feedback.

This project allows you to control and monitor your Tuya heat pump device through Home Assistant — supports both Cloud and Local (push) connection modes.

---

## Prerequisites

### Enabling Tuya IoT Cloud Service

To use this integration, you need to create a project in the Tuya IoT Platform, grant API access, and link your device to the project.

**Steps:**

1. Log in to ***[Tuya IoT Platform](https://iot.tuya.com/)***.
2. Go to ***Cloud > Project Management*** and create a new project or select an existing one.
3. Select the ***Devices*** tab:
   - If your devices are already listed, proceed to the next step.
   - If you have no devices yet, open the ***Link App Account*** tab below. Click the ***Add App Account*** button on the right, then select ***Tuya App Account Authorization***. Scan the QR code using your Tuya mobile app and grant permission. Your devices will then appear.
4. Click on the ***Service API*** tab above, then click the ***Go to Authorize*** button and add the following APIs to your project:
   - ***IoT Core***
   - ***Smart Home Basic Service***
   - ***Device Status Notification***
   - ***Authorization Token Management***
5. Retrieve your ***Access ID*** and ***Access Secret*** from the project panel.

> ⚠️ **Important:** The integration will not work without API authorization and device linking.

---

## Installation

[![Open your Home Assistant instance and open a repository inside the Home Assistant Community Store](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=Korkuttum&repository=tuya_heat_pump&category=integration)

### Method 1: Installation via HACS (Recommended)

1. Make sure you have **HACS** installed in your Home Assistant instance.
2. Go to **HACS** → **Integrations**.
3. Click the search icon in the top right and search for **"Tuya Heat Pump"**.
4. Click **Download** on the integration.
5. Restart Home Assistant.

### Method 2: Manual Installation

1. Download the latest release from the [GitHub repository](https://github.com/Korkuttum/tuya_heat_pump).
2. Extract the files and copy the `tuya_heat_pump` folder into your Home Assistant `custom_components` directory.
3. Restart Home Assistant.
---

## Configuration

After installation, restart Home Assistant and follow these steps:

1. Go to “Settings > Devices & Services”.
2. Click “Add Integration”.
3. Search for and select “Tuya Heat Pump”.
4. For Cloud mode: enter your Tuya IoT Platform credentials:
    - Access ID
    - Access Secret
    - Device ID
5. For Local mode: switch the Connection Type to “Local” and enter:
    - Device IP
    - Local Key
    - Protocol (e.g. 3.3 / 3.4)
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
