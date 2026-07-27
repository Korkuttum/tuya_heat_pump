# test/ — Diagnostic & Setup Scripts

Standalone scripts for onboarding new devices, debugging, and finding
local network credentials. None of these are part of the Home
Assistant integration itself — they're run manually, on your own
computer, outside of Home Assistant. Each one prints its results to
the console and/or writes an output file you can attach to a GitHub
issue.

| Script | What it's for |
|---|---|
| [`tuya_api_test.py`](https://github.com/Korkuttum/tuya_heat_pump/blob/main/test/tuya_api_test.py) | **Start here for a new device.** Dumps everything Tuya's cloud API knows about your device. |
| [`lokal_key_extractor.py`](https://github.com/Korkuttum/tuya_heat_pump/blob/main/test/lokal_key_extractor.py) | Tries to find your device's Local Key, needed for local (LAN) mode. |
| [`tuya_dps_explorer.py`](https://github.com/Korkuttum/tuya_heat_pump/blob/main/test/tuya_dps_explorer.py) | Reads raw values directly from the device over your local network (no cloud/no Access ID needed). |
| [`raw_explorer.py`](https://github.com/Korkuttum/tuya_heat_pump/blob/main/test/raw_explorer.py) | Live GUI for decoding `raw` type data-points (hidden settings like target temperature). |

---

## 1. `tuya_api_test.py`

The first thing to run for **any new device or model support
request**. Connects to Tuya's cloud API with your Access ID/Access
Key and pulls both the device's current live property values and its
full schema (every DP code, type, access mode, min/max, and — often
more reliable than the English code name — the real Chinese name
Tuya uses internally).

**Requirements:** `pip install requests`

**Step by step:**
1. Run the script.
2. Enter your **Access ID**, **Access Key**, **region** (`eu`/`us`/`cn`/`in`,
   or a full URL), and **Device ID** when prompted.
3. It prints a short summary of every property to the console, and
   writes a `tuya_device_data_<timestamp>.txt` file in the same folder.
4. Attach that whole `.txt` file when opening a device-support issue —
   it's normally enough on its own to build a complete model mapping.

## 2. `lokal_key_extractor.py`

Tries to retrieve your device's **Local Key** — a per-device secret
needed for local (LAN) mode, separate from your account's Access
ID/Access Key. You'll need this for `tuya_dps_explorer.py` below, and
for setting up the integration itself in local mode.

**Requirements:** `pip install requests`

**Step by step:**
1. Run the script.
2. Enter the same Access ID, Access Key, region, and Device ID as above.
3. It prints the device's name and Local Key, if available.

**Heads up:** Tuya has hidden the Local Key for most non-gateway
devices since around 2022 for security reasons, so this often comes
back empty. If it does, the script prints a few alternatives to try:
`python -m tinytuya wizard`, the Home Assistant LocalTuya integration,
or extracting it from the Smart Life app's own local database (via an
emulator + an older app version).

## 3. `tuya_dps_explorer.py`

Reads a device's raw DP values directly over the **local network**
(LAN), bypassing the cloud entirely — no Access ID/Access Key needed
at all here, just your device's Local Key and it being on the same
network as your computer. Useful for comparing local vs. cloud values
for the same DP (some devices report differently depending on
connection type), or just confirming what a device *actually* sends.

**Requirements:** `pip install tinytuya`

**Step by step:**
1. Run the script — it scans your local network and lists every Tuya
   device it finds (IP, Device ID, protocol version, product key).
2. Pick the number matching your device.
3. Enter its **Local Key** (from step 2 above, if you have it).
4. It prints the complete raw DPS data — every DP ID, its value, and
   its Python type.

## 4. `raw_explorer.py`

A live-updating GUI for reverse-engineering `raw` type data-points —
the ones Tuya's API doesn't explain, just calls "raw" binary data.
Many devices hide real settings in there (most commonly: the target
temperature setpoint, when it's missing from the normal DP list).

**Requirements:** none to install manually — `requests` installs
itself automatically on first run. `tkinter` (the GUI toolkit) comes
bundled with the standard Windows/macOS Python installer.

**Step by step:**
1. Run the script (from a terminal if possible, so you'll see any
   errors printed instead of a window just closing silently — there's
   also a `raw_explorer.log` file written next to the script with a
   full trace either way).
2. A connection screen appears — enter the same Access ID, Access Key,
   region, and Device ID as `tuya_api_test.py`, then connect.
3. The main window opens: a live-updating table of every DP, including
   the raw ones broken down into individual fields you can inspect.
4. **This is the important part — the tool is passive.** With the
   window still open, go into the **Tuya Smart / Smart Life app** and
   actually change something on the device (target temperature, a
   mode, a fan limit — whatever you're trying to locate). Leaving the
   tool open without touching the device in the app won't find
   anything.
5. Watch the table right as you make the change — whichever field's
   value visibly shifts at that exact moment is very likely the thing
   you just adjusted.
6. Label it: give it a name, unit, and scale (if it needs
   dividing/multiplying to get a sensible number). For writable (`rw`)
   fields, also pick what kind of Home Assistant entity it should
   become (number, select, switch, or text) and set its
   min/max/step/options.
7. Export — this generates a `RAW_FIELD_TYPES_<device_id>_<timestamp>.py`
   file. Attach that to your issue; if you've found and labeled
   several fields in one sitting, sending them all together is much
   more efficient than one at a time.

**Common gotcha:** if a field's value jumps by exactly 65536 (or a
multiple of it) between two readings, that usually means two
*different* 16-bit values are packed into what looks like one 32-bit
field — it needs splitting into upper/lower halves rather than being
treated as one number. Ask if you're not sure how to handle it, we
can help work it out from your readings.
