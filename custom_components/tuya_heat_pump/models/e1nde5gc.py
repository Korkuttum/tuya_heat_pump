"""Model mapping for Effecta Air-IQ R290 Heat Pump (e1nde5gc)."""

MODEL_NAME = "Effecta Air-IQ R290 Heat Pump (e1nde5gc)"
# ====================================================
# Effecta Air-IQ R290 @mnoxfeld, issue #83
# Product code: PW58382-4 (products_id, dp 180) — the "PW" prefix and the
# device id's "pwvx" suffix both point at this being a Power World OEM
# unit, same family as e1k5wjuc (Power World R290 Full DC).
#
# Built from a single cloud properties + model dump (no live device
# access, no raw_explorer.py run yet). DP 1, 2, 5, 6, 110, 111, 112, 125,
# 130, 180 and 15 match e1k5wjuc's own schema exactly (same codes, same
# enum ranges, same accessMode), so SWITCH/SELECT/NUMBER/SENSOR/
# BINARY_SENSOR below are taken directly from this device's own typeSpec —
# not guessed from e1k5wjuc.
#
# UNRESOLVED — raw parameter groups: this device has no field-level
# breakdown for any of its "raw" DPs in Tuya's model metadata (same
# situation as e1kx07j4/Lunna, issue #78). The raw group *names* are
# different from e1k5wjuc's (status_parameter_group_1/2,
# parameter_group_23) — this device uses:
#   - pg120_status   (dp 101, ro) — 240-byte status block. NOTE: despite
#     "120" in the name this decodes as 120 × int16_be fields (240 / 2),
#     not int32_be — the one sample dump has small plausible-looking
#     values (30s and 300s range) only when read as int16.
#   - pg60_user_1    (dp 120, rw) — 60 × int32_be user parameter group 1
#   - pg60_user_2    (dp 121, rw) — 60 × int32_be user parameter group 2
#   - pg60_factory_1 (dp 122, rw) — 60 × int32_be factory parameter group 1
#   - pg60_factory_2 (dp 123, rw) — 60 × int32_be factory parameter group 2
#   - pg60_factory_3 (dp 124, rw) — 60 × int32_be factory parameter group 3
#   - pg_es          (dp 140, rw) — 20 × int32_be "electricity statistics"
#     group; the one sample has a device-clock-shaped tail
#     (…, 2026, 9, 10, 21, 19, 39, 0, 0, …) but no confirmed field map
#   - pg80_fault     (dp 190, ro) — 80 × uint8 fault detail block, all
#     zero in the one sample (no active faults) so nothing to anchor a
#     field map to yet
# All live sensors (water/ambient temps, compressor, fan speeds, power,
# etc. — presumably packed into pg120_status, going by e1k5wjuc/e1kx07j4
# precedent) are unavailable until these are mapped. To find them: run
# test/raw_explorer.py against the real device — it decodes each raw DP
# live, highlights which fields change, and can export a ready-to-paste
# SENSOR_TYPES/NUMBER_TYPES snippet once a field is identified. Paste that
# snippet at the bottom of this file once available.
#
# Setpoint ranges (wth_set 28-176, heating_set 15-176, cooling_set 7-86)
# are this device's own typeSpec min/max, taken as-is — unlike e1kx07j4's
# heat_settemp, these are not an obvious template placeholder (they differ
# per DP). They're wide enough to span both °C and °F, though, so if the
# real on-device range turns out narrower once confirmed via the Smart
# Life app, tighten these.
# ====================================================

# ====================================================
# SENSOR TYPES (read-only value - accessMode: "ro")
# ====================================================
SENSOR_TYPES = {
    # Fault Description (dp_id: 15) — Tuya's own schema for this device
    # lists a single bitmap label: Er09 (communication fault).
    "fault": {
        "dp_id": 15,
        "code": "fault",
        "name": "Fault Description",
        "icon": "mdi:alert-circle",
        "conversion": (
            "', '.join(n for b, n in [(1,'Er09')] if value & b) or 'OK'"
        ),
    },
    # Product ID (dp_id: 180)
    "products_id": {
        "dp_id": 180,
        "code": "products_id",
        "name": "Product ID",
        "icon": "mdi:identifier",
    },
}

# ====================================================
# BINARY SENSOR TYPES (read-only bool/bitmap - accessMode: "ro")
# ====================================================
BINARY_SENSOR_TYPES = {
    # Fault Status (dp_id: 15)
    "fault": {
        "dp_id": 15,
        "code": "fault",
        "name": "Fault Status",
        "device_class": "problem",
        "conversion": "value != 0",
    },
}

# ====================================================
# SWITCH TYPES (read-write bool - accessMode: "rw"/"wr")
# ====================================================
SWITCH_TYPES = {
    # Power Switch (dp_id: 1)
    "switch": {
        "dp_id": 1,
        "code": "switch",
        "name": "Power",
        "icon": "mdi:power",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']",
    },
    # Reset to Default (dp_id: 125) - accessMode: "wr"; Tuya's own
    # description notes this only takes effect while the unit is off.
    "reset": {
        "dp_id": 125,
        "code": "reset",
        "name": "Reset to Default",
        "icon": "mdi:restore",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']",
    },
}

# ====================================================
# NUMBER TYPES (read-write value - accessMode: "rw"/"wr")
# ====================================================
NUMBER_TYPES = {
    # Hot Water Temperature Setpoint (dp_id: 110)
    "wth_set": {
        "dp_id": 110,
        "code": "wth_set",
        "name": "Hot Water Temperature",
        "icon": "mdi:water-thermometer",
        "unit": "°C",
        "min_value": 28.0,
        "max_value": 176.0,
        "step": 1.0,
        "api_conversion": "value",
    },
    # Heating Temperature Setpoint (dp_id: 111)
    "heating_set": {
        "dp_id": 111,
        "code": "heating_set",
        "name": "Heating Temperature",
        "icon": "mdi:thermostat",
        "unit": "°C",
        "min_value": 15.0,
        "max_value": 176.0,
        "step": 1.0,
        "api_conversion": "value",
    },
    # Cooling Temperature Setpoint (dp_id: 112)
    "cooling_set": {
        "dp_id": 112,
        "code": "cooling_set",
        "name": "Cooling Temperature",
        "icon": "mdi:snowflake",
        "unit": "°C",
        "min_value": 7.0,
        "max_value": 86.0,
        "step": 1.0,
        "api_conversion": "value",
    },
    # Manual Defrost (dp_id: 130) - accessMode: "wr"
    "hdef": {
        "dp_id": 130,
        "code": "hdef",
        "name": "Manual Defrost",
        "icon": "mdi:snowflake-melt",
        "unit": "",
        "min_value": 1.0,
        "max_value": 8.0,
        "step": 1.0,
        "api_conversion": "value",
    },
}

# ====================================================
# SELECT TYPES (read-write enum - accessMode: "rw")
# ====================================================
SELECT_TYPES = {
    # Operation Mode (dp_id: 2) - smart, strong, mute
    "mode": {
        "dp_id": 2,
        "code": "mode",
        "name": "Operation Mode",
        "icon": "mdi:hvac",
        "options": {
            "smart": "Smart",
            "strong": "Strong",
            "mute": "Mute",
        },
    },
    # Work Mode (dp_id: 5) - wth, heat, cool, wth_heat, wth_cool
    "work_mode": {
        "dp_id": 5,
        "code": "work_mode",
        "name": "Work Mode",
        "icon": "mdi:cog",
        "options": {
            "wth": "Hot Water",
            "heat": "Heating",
            "cool": "Cooling",
            "wth_heat": "Hot Water + Heating",
            "wth_cool": "Hot Water + Cooling",
        },
    },
    # Temperature Unit (dp_id: 6) - c, f
    "temp_unit_convert": {
        "dp_id": 6,
        "code": "temp_unit_convert",
        "name": "Temperature Unit",
        "icon": "mdi:thermometer",
        "options": {
            "c": "Celsius",
            "f": "Fahrenheit",
        },
    },
}

# ====================================================
# Raw-field entries from test/raw_explorer.py go here once available.
#
# Paste the exported snippet below this line, then merge each block into
# the matching dict above via .update() — see e1kx07j4.py or ew8plw.py for
# the exact pattern raw_explorer.py's export uses.
# ====================================================
