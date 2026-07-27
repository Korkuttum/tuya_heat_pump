# test/ — Diagnostic & Setup Scripts

Standalone scripts used for onboarding new devices, debugging, and
finding local network credentials. None of these are part of the
Home Assistant integration itself — they're run manually, on your own
computer, outside of Home Assistant.

| Script | What it's for |
|---|---|
| [`tuya_api_test.py`](#tuya_api_testpy) | **Start here for a new device.** Dumps everything Tuya's cloud API knows about your device. |
| [`tuya_dps_explorer.py`](#tuya_dps_explorerpy) | Reads raw values directly from the device over your local network (no cloud). |
| [`raw_explorer.py`](#raw_explorerpy) | Live GUI for decoding `raw` type data-points (hidden settings like target temperature). |
| [`lokal_key_extractor.py`](#lokal_key_extractorpy) | Helps you find your device's Local Key, needed for local (LAN) mode setup. |

---

## `tuya_api_test.py`

The first thing to run for **any new device or model support
request**. Connects to Tuya's cloud API with your Access ID/Access
Key and pulls:

- The device's current live property values
- The device's full schema (every DP code, type, access mode, min/max,
  and — critically — the real Chinese name Tuya uses internally,
  which is often far more reliable than the English `code` name)

**Usage:** run it, enter your Access ID, Access Key, region, and
Device ID when prompted. It writes a `tuya_device_data_<timestamp>.txt`
file — attach that whole file when opening a device-support issue.
This one file is normally enough to build a complete model mapping.

## `tuya_dps_explorer.py`

Reads a device's raw DP values directly over the **local network**
(LAN), bypassing the cloud entirely. Useful for:

- Comparing local vs. cloud values for the same DP (some devices
  report differently depending on the connection type)
- Confirming what a device *actually* sends when cloud data looks
  inconsistent or you're troubleshooting local mode specifically

**Usage:** run it, it scans your network for Tuya devices and lists
them. Pick yours, enter its Local Key (see `lokal_key_extractor.py`
below if you don't have this yet), and it prints every DP's raw
value and type.

## `raw_explorer.py`

A live-updating GUI for reverse-engineering `raw` type data-points —
the ones Tuya's API doesn't explain, just calls "raw" binary data.
Many devices hide real settings in there (most commonly: the target
temperature setpoint, when it's missing from the normal DP list).

**Usage:** run it, connect with the same Access ID/Access Key/Device
ID as above. With the tool's window open, actively change something
on the device via the Tuya/Smart Life app (a setpoint, a mode, a fan
limit) and watch which raw field changes at that exact moment — that's
the one you're looking for. Label it (name, unit, scale, and for
writable fields, what kind of entity it should become), then export —
this produces a `RAW_FIELD_TYPES_<device_id>_<timestamp>.py` file
ready to merge into a model file.

**Important:** this tool is passive — it only reacts to changes you
actively make while it's running. Leaving it open without touching
the device in the app won't find anything.

**Common gotcha:** if a field's value jumps by exactly 65536 (or a
multiple of it) between two readings, that usually means two
*different* 16-bit values are packed into what looks like one 32-bit
field — it needs splitting into upper/lower halves rather than being
treated as one number. Ask if you're not sure, we can help work it
out from your readings.

## `lokal_key_extractor.py`

Helps retrieve your device's **Local Key** — a per-device secret
required to connect in local (LAN) mode, separate from your account's
Access ID/Access Key. You'll need this for `tuya_dps_explorer.py`
above, and for setting up the integration itself in local mode.

**Usage:** run it and follow the prompts (same Tuya credentials as
the other scripts). If you run into issues with this one specifically,
flag it in your issue and we'll walk through it together.
