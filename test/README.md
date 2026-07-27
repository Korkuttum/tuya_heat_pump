<div align="center">

# 🛠️ test/ — Diagnostic & Setup Scripts

**Standalone helper scripts for onboarding new devices, debugging, and finding local network credentials**

![Python](https://img.shields.io/badge/Python-3.9%2B-3776AB?style=flat-square&logo=python&logoColor=white)
![Standalone](https://img.shields.io/badge/Runs-Outside%20HA-orange?style=flat-square)
![License](https://img.shields.io/badge/Part%20of-tuya__heat__pump-blue?style=flat-square)

None of these are part of the Home Assistant integration itself — they're run **manually, on your own computer**, outside of Home Assistant. Each one prints its results to the console and/or writes an output file you can attach to a GitHub issue.

</div>

<br>

## 📑 Scripts at a Glance

| | Script | Purpose | Requirements |
|:---:|---|---|---|
| 🚀 | [`tuya_api_test.py`](#-1-tuya_api_testpy) | **Start here** for a new device | `requests` |
| 🔑 | [`lokal_key_extractor.py`](#-2-lokal_key_extractorpy) | Find your device's Local Key | `requests` |
| 📡 | [`tuya_dps_explorer.py`](#-3-tuya_dps_explorerpy) | Read raw values over LAN | `tinytuya` |
| 🧩 | [`raw_explorer.py`](#-4-raw_explorerpy) | Decode hidden raw data-points (GUI) | none (self-installs) |

<br>

---

<br>

<details open>
<summary><h3>🚀 1. <code>tuya_api_test.py</code></h3><sub>Pulls your device's full cloud schema and live values — the first script to run for any new device.</sub></summary>

> **Start here for any new device or model support request.**

Connects to Tuya's cloud API with your Access ID/Access Key and pulls both the device's current live property values and its full schema — every DP code, type, access mode, min/max, and (often more reliable than the English code name) the real Chinese name Tuya uses internally.

```bash
pip install requests
```

**📋 Step by step**

| Step | Action |
|:---:|---|
| 1 | Run the script |
| 2 | Enter your **Access ID**, **Access Key**, **region** (`eu`/`us`/`cn`/`in`, or a full URL), and **Device ID** when prompted |
| 3 | It prints a summary of every property to the console, and writes a `tuya_device_data_<timestamp>.txt` file in the same folder |
| 4 | Attach that whole `.txt` file when opening a device-support issue — it's usually enough on its own to build a complete model mapping |

📎 [**View script →**](https://github.com/Korkuttum/tuya_heat_pump/blob/main/test/tuya_api_test.py)

</details>

<br>

<details>
<summary><h3>🔑 2. <code>lokal_key_extractor.py</code></h3><sub>Tries to recover your device's Local Key, needed for LAN (local) mode.</sub></summary>

Tries to retrieve your device's **Local Key** — a per-device secret needed for local (LAN) mode, separate from your account's Access ID/Access Key. You'll need this for `tuya_dps_explorer.py` below, and for setting up the integration itself in local mode.

```bash
pip install requests
```

**📋 Step by step**

| Step | Action |
|:---:|---|
| 1 | Run the script |
| 2 | Enter the same Access ID, Access Key, region, and Device ID as above |
| 3 | It prints the device's name and Local Key, if available |

> ⚠️ **Heads up:** Tuya has hidden the Local Key for most non-gateway devices since around 2022 for security reasons, so this often comes back empty. If it does, the script suggests a few alternatives: `python -m tinytuya wizard`, the Home Assistant LocalTuya integration, or extracting it from the Smart Life app's own local database (via an emulator + an older app version).

📎 [**View script →**](https://github.com/Korkuttum/tuya_heat_pump/blob/main/test/lokal_key_extractor.py)

</details>

<br>

<details>
<summary><h3>📡 3. <code>tuya_dps_explorer.py</code></h3><sub>Reads raw DP values straight off your local network — no cloud credentials needed.</sub></summary>

Reads a device's raw DP values directly over the **local network (LAN)**, bypassing the cloud entirely — no Access ID/Access Key needed here, just your device's Local Key and it being on the same network as your computer. Useful for comparing local vs. cloud values for the same DP, or just confirming what a device *actually* sends.

```bash
pip install tinytuya
```

**📋 Step by step**

| Step | Action |
|:---:|---|
| 1 | Run the script — it scans your local network and lists every Tuya device it finds (IP, Device ID, protocol version, product key) |
| 2 | Pick the number matching your device |
| 3 | Enter its **Local Key** (from step 2 above, if you have it) |
| 4 | It prints the complete raw DPS data — every DP ID, its value, and its Python type |

📎 [**View script →**](https://github.com/Korkuttum/tuya_heat_pump/blob/main/test/tuya_dps_explorer.py)

</details>

<br>

<details>
<summary><h3>🧩 4. <code>raw_explorer.py</code></h3><sub>Live GUI for decoding hidden "raw" data-points, like a missing target temperature setting.</sub></summary>

A live-updating **GUI** for reverse-engineering `raw` type data-points — the ones Tuya's API doesn't explain, just calls "raw" binary data. Many devices hide real settings in there (most commonly: the target temperature setpoint, when it's missing from the normal DP list).

> 💡 **Requirements:** none to install manually — `requests` installs itself automatically on first run. `tkinter` (the GUI toolkit) comes bundled with the standard Windows/macOS Python installer.

**📋 Step by step**

| Step | Action |
|:---:|---|
| 1 | Run the script (preferably from a terminal, so errors print instead of the window silently closing — a `raw_explorer.log` file is also written next to the script either way) |
| 2 | A connection screen appears — enter the same Access ID, Access Key, region, and Device ID as `tuya_api_test.py`, then connect |
| 3 | The main window opens: a live-updating table of every DP, including raw ones broken into individual inspectable fields |
| 4 | **The important part — the tool is passive.** With the window open, go into the **Tuya Smart / Smart Life app** and actually change something on the device (target temp, a mode, a fan limit). Nothing will be found if you don't touch the device in the app |
| 5 | Watch the table as you make the change — whichever field visibly shifts at that exact moment is very likely the thing you just adjusted |
| 6 | Label it: name, unit, and scale (if it needs dividing/multiplying). For writable (`rw`) fields, also pick the Home Assistant entity type (number, select, switch, text) and set min/max/step/options |
| 7 | Export → generates `RAW_FIELD_TYPES_<device_id>_<timestamp>.py`. Attach it to your issue — sending several labeled fields together is much more efficient than one at a time |

> 🧠 **Common gotcha:** if a field's value jumps by exactly 65536 (or a multiple of it) between two readings, that usually means two *different* 16-bit values are packed into what looks like one 32-bit field — it needs splitting into upper/lower halves rather than being treated as one number. Ask if you're not sure how to handle it, we can help work it out from your readings.

📎 [**View script →**](https://github.com/Korkuttum/tuya_heat_pump/blob/main/test/raw_explorer.py)

</details>

<br>

---

<div align="center">

💬 Questions or stuck on a device? [Open an issue](https://github.com/Korkuttum/tuya_heat_pump/issues) and attach whatever output file the relevant script produced.

</div>
