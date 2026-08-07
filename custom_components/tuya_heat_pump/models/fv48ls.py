"""Model mapping for Alsavo by Zealux Heat Pump (modelId: fv48ls)."""

MODEL_NAME = "Alsavo by Zealux Heat Pump (fv48ls)"
# ====================================================
# Alsavo by Zealux @jebizoe
# modelId: fv48ls
# Notes:
#   - Schema decoded from live Tuya device model dump (device_id
#     bfea58b9ec3e22430duzxz), NOT copy-pasted from another model —
#     dp_ids/codes here differ completely from the previous draft file
#     that was based on the Adlar Castra template (see Golden Rule #1
#     in CONTRIBUTING.md: that draft's dict keys pointed at the wrong
#     DPs entirely for this device).
#   - All Chinese `name` fields were decoded and cross-checked against
#     each `code` before naming anything (Golden Rule #2). A few codes
#     are genuinely self-explanatory in English (SET_TANK_TEMP,
#     RUN_MODE, etc.) and matched their Chinese name 1:1 — verified,
#     not assumed.
#   - Most system/refrigerant temperature DPs (113-120, 134, 136) are
#     schema scale=1 -> raw value needs /10 (e.g. WATER_BACK_TEMP raw
#     204 -> 20.4°C). IPM_TEMP (125) and temp_current (16) are scale=0,
#     no conversion. Confirmed against the live sample dump, where
#     WATER_BACK_TEMP (20.4°C) and WATER_OUT_TEMP (20.3°C) land close
#     together as expected for a return/supply water pair.
#   - Several diagnostic DPs (WATER_TANK_TEMP, Economizer_i_temp,
#     Economizer_o_temp) read -400 (-> -40.0°C) in the sample dump.
#     That's almost certainly a "sensor not installed/not active"
#     placeholder rather than a real reading (economizer circuit not
#     in use on this unit) — kept as normal sensors since we don't have
#     confirmation either way; flagging here so nobody "fixes" it later
#     without checking real data first per the CONTRIBUTING.md rule on
#     not guessing.
#   - fault_num (104) is declared type "value" (0-1000), not a bitmap
#     like WOPOLTOP's `fault` — so no per-bit decode here, just the raw
#     code, plus a binary_sensor quick-view (value != 0) matching the
#     convention used elsewhere (e.g. WOPOLTOP, Reclaim).
#   - PROTECT_FLAG / pro_flag1-4 have huge declared ranges
#     (+/-2147483647) suggesting they may be bitmasks or raw fault
#     codes, but there's no per-bit schema info to decode them safely
#     (unlike WOPOLTOP's documented 23-bit fault map) — kept as plain
#     diagnostic sensors only. Don't add a bitmap "conversion" for
#     these without real confirmed data (see CONTRIBUTING.md: don't
#     guess ranges/decodes).
#   - RUN_MODE (110) is a read-only enum (COOL/HEAT) reflecting actual
#     running state, distinct from the user-facing `mode` (2, rw,
#     cold/heating - target selection) and `work_mode` (5, rw,
#     smart/silent). Exposed as a sensor with an options map, not a
#     select, since it can't be written.
# ====================================================

SENSOR_TYPES = {
    # ---- Core temperature ----
    "temp_current": {
        "dp_id": 16,
        "code": "temp_current",
        "name": "Current Temperature",
        "unit": "°C",
        "icon": "mdi:thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
    },
    "temp_current_f": {
        "dp_id": 35,
        "code": "temp_current_f",
        "name": "Current Temperature (F)",
        "unit": "°F",
        "icon": "mdi:thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
    },

    # ---- Fault / status ----
    "fault_num": {
        "dp_id": 104,
        "code": "fault_num",
        "name": "Fault Code",
        "icon": "mdi:alert-circle",
        "state_class": "measurement",
    },
    "RUN_MODE": {
        "dp_id": 110,
        "code": "RUN_MODE",
        "name": "Running Mode",
        "icon": "mdi:hvac",
        "options": {
            "COOL": "Cooling",
            "HEAT": "Heating",
        },
    },

    # ---- Compressor / performance ----
    "RUN_FREQUENT": {
        "dp_id": 111,
        "code": "RUN_FREQUENT",
        "name": "Running Frequency",
        "unit": "Hz",
        "icon": "mdi:cosine-wave",
        "state_class": "measurement",
    },
    "RUN_CURRENT": {
        "dp_id": 112,
        "code": "RUN_CURRENT",
        "name": "Running Current",
        "unit": "A",
        "icon": "mdi:current-ac",
        "device_class": "current",
        "state_class": "measurement",
        "conversion": "value / 10",
    },
    "TRAGE_FREQUENT": {
        "dp_id": 123,
        "code": "TRAGE_FREQUENT",
        "name": "Target Frequency",
        "unit": "Hz",
        "icon": "mdi:cosine-wave",
        "state_class": "measurement",
    },

    # ---- Water circuit temperatures ----
    "WATER_BACK_TEMP": {
        "dp_id": 113,
        "code": "WATER_BACK_TEMP",
        "name": "Water Return Temperature",
        "unit": "°C",
        "icon": "mdi:water-thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
        "conversion": "value / 10",
    },
    "WATER_TANK_TEMP": {
        "dp_id": 114,
        "code": "WATER_TANK_TEMP",
        "name": "Tank Water Temperature",
        "unit": "°C",
        "icon": "mdi:water-thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
        "conversion": "value / 10",
    },
    "WATER_OUT_TEMP": {
        "dp_id": 115,
        "code": "WATER_OUT_TEMP",
        "name": "Water Supply Temperature",
        "unit": "°C",
        "icon": "mdi:water-thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
        "conversion": "value / 10",
    },

    # ---- Outdoor unit / refrigerant circuit temperatures ----
    "SYS_PQ_TEMP": {
        "dp_id": 116,
        "code": "SYS_PQ_TEMP",
        "name": "Discharge Temperature",
        "unit": "°C",
        "icon": "mdi:thermometer-alert",
        "device_class": "temperature",
        "state_class": "measurement",
        "conversion": "value / 10",
    },
    "OUT_TEMP": {
        "dp_id": 117,
        "code": "OUT_TEMP",
        "name": "Outdoor Ambient Temperature",
        "unit": "°C",
        "icon": "mdi:home-thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
        "conversion": "value / 10",
    },
    "SYS_PG_TEMP": {
        "dp_id": 118,
        "code": "SYS_PG_TEMP",
        "name": "Outdoor Coil Temperature",
        "unit": "°C",
        "icon": "mdi:thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
        "conversion": "value / 10",
    },
    "SYS_BACK_TEMP": {
        "dp_id": 119,
        "code": "SYS_BACK_TEMP",
        "name": "Return Gas Temperature",
        "unit": "°C",
        "icon": "mdi:thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
        "conversion": "value / 10",
    },
    "SYS_JIEL_TEMP": {
        "dp_id": 120,
        "code": "SYS_JIEL_TEMP",
        "name": "Post-Throttle Temperature",
        "unit": "°C",
        "icon": "mdi:thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
        "conversion": "value / 10",
    },
    "IPM_TEMP": {
        "dp_id": 125,
        "code": "IPM_TEMP",
        "name": "IPM Module Temperature",
        "unit": "°C",
        "icon": "mdi:thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
    },

    # ---- Economizer (may read -40.0°C / not active on units without it) ----
    "Economizer_i_temp": {
        "dp_id": 134,
        "code": "Economizer_i_temp",
        "name": "Economizer Inlet Temperature",
        "unit": "°C",
        "icon": "mdi:thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
        "conversion": "value / 10",
    },
    "Economizer_o_temp": {
        "dp_id": 136,
        "code": "Economizer_o_temp",
        "name": "Economizer Outlet Temperature",
        "unit": "°C",
        "icon": "mdi:thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
        "conversion": "value / 10",
    },

    # ---- Valve positions ----
    "MIAN_EVI_STEP": {
        "dp_id": 121,
        "code": "MIAN_EVI_STEP",
        "name": "Main EEV Position",
        "icon": "mdi:pipe-valve",
        "state_class": "measurement",
    },
    "EVI_STEP": {
        "dp_id": 124,
        "code": "EVI_STEP",
        "name": "EVI Valve Position",
        "icon": "mdi:pipe-valve",
        "state_class": "measurement",
    },

    # ---- Electrical ----
    "DCBUS_VOL": {
        "dp_id": 130,
        "code": "DCBUS_VOL",
        "name": "DC Bus Voltage",
        "unit": "V",
        "icon": "mdi:lightning-bolt",
        "device_class": "voltage",
        "state_class": "measurement",
    },
    "ACIN_VOL": {
        "dp_id": 131,
        "code": "ACIN_VOL",
        "name": "AC Input Voltage",
        "unit": "V",
        "icon": "mdi:lightning-bolt",
        "device_class": "voltage",
        "state_class": "measurement",
    },

    # ---- Protection flags (raw, undecoded - see notes above) ----
    "PROTECT_FLAG": {
        "dp_id": 122,
        "code": "PROTECT_FLAG",
        "name": "Protection Code",
        "icon": "mdi:shield-alert",
        "state_class": "measurement",
    },
    "pro_flag1": {
        "dp_id": 127,
        "code": "pro_flag1",
        "name": "Protection Flag 1",
        "icon": "mdi:shield-alert",
        "state_class": "measurement",
    },
    "pro_flag2": {
        "dp_id": 129,
        "code": "pro_flag2",
        "name": "Protection Flag 2",
        "icon": "mdi:shield-alert",
        "state_class": "measurement",
    },
    "pro_flag3": {
        "dp_id": 132,
        "code": "pro_flag3",
        "name": "Protection Flag 3",
        "icon": "mdi:shield-alert",
        "state_class": "measurement",
    },
    "pro_flag4": {
        "dp_id": 133,
        "code": "pro_flag4",
        "name": "Protection Flag 4",
        "icon": "mdi:shield-alert",
        "state_class": "measurement",
    },
}

# ====================================================
# BINARY SENSOR TYPES
# ====================================================
BINARY_SENSOR_TYPES = {
    "fault_num": {
        "dp_id": 104,
        "code": "fault_num",
        "name": "Fault Status",
        "device_class": "problem",
        "conversion": "value != 0",
    },
}

# ====================================================
# SWITCH TYPES
# ====================================================
SWITCH_TYPES = {
    "switch": {
        "dp_id": 1,
        "code": "switch",
        "name": "Power",
        "icon": "mdi:power",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']",
    },
}

# ====================================================
# NUMBER TYPES
# ====================================================
NUMBER_TYPES = {
    "temp_set": {
        "dp_id": 4,
        "code": "temp_set",
        "name": "Heating Temperature Setpoint",
        "icon": "mdi:thermostat",
        "unit": "°C",
        "min_value": 15.0,
        "max_value": 60.0,
        "step": 1.0,
        "api_conversion": "int(value)",
    },
    "SET_TANK_TEMP": {
        "dp_id": 103,
        "code": "SET_TANK_TEMP",
        "name": "Tank Temperature Setpoint",
        "icon": "mdi:water-thermometer",
        "unit": "°C",
        "min_value": 20.0,
        "max_value": 60.0,
        "step": 1.0,
        "api_conversion": "int(value)",
    },
    "SET_COOL_TEMP": {
        "dp_id": 105,
        "code": "SET_COOL_TEMP",
        "name": "Cooling Temperature Setpoint",
        "icon": "mdi:thermostat",
        "unit": "°C",
        "min_value": 5.0,
        "max_value": 35.0,
        "step": 1.0,
        "api_conversion": "int(value)",
    },
    "SET_DEFIN_TEMP": {
        "dp_id": 106,
        "code": "SET_DEFIN_TEMP",
        "name": "Defrost Entry Coil Temperature",
        "icon": "mdi:snowflake-thermometer",
        "unit": "°C",
        "min_value": -20.0,
        "max_value": 20.0,
        "step": 1.0,
        "api_conversion": "int(value)",
    },
    "SET_DEFOUT_TEMP": {
        "dp_id": 107,
        "code": "SET_DEFOUT_TEMP",
        "name": "Defrost Exit Coil Temperature",
        "icon": "mdi:snowflake-thermometer",
        "unit": "°C",
        "min_value": 1.0,
        "max_value": 50.0,
        "step": 1.0,
        "api_conversion": "int(value)",
    },
    "SET_DEF_LOOPTIME": {
        "dp_id": 108,
        "code": "SET_DEF_LOOPTIME",
        "name": "Defrost Cycle Interval",
        "icon": "mdi:timer-sync",
        "unit": "min",
        "min_value": 1.0,
        "max_value": 120.0,
        "step": 1.0,
        "api_conversion": "int(value)",
    },
    "SET_DEF_MAXTIME": {
        "dp_id": 109,
        "code": "SET_DEF_MAXTIME",
        "name": "Max Defrost Duration",
        "icon": "mdi:timer",
        "unit": "min",
        "min_value": 1.0,
        "max_value": 25.0,
        "step": 1.0,
        "api_conversion": "int(value)",
    },
    "Refresh_cycle": {
        "dp_id": 135,
        "code": "Refresh_cycle",
        "name": "Refresh Cycle",
        "icon": "mdi:timer-refresh",
        "min_value": 1.0,
        "max_value": 600.0,
        "step": 1.0,
        "api_conversion": "int(value)",
    },
    "set_silent_frequent": {
        "dp_id": 140,
        "code": "set_silent_frequent",
        "name": "Silent Mode Frequency",
        "icon": "mdi:cosine-wave",
        "unit": "Hz",
        "min_value": 30.0,
        "max_value": 80.0,
        "step": 1.0,
        "api_conversion": "int(value)",
    },
    "set_silent_speed": {
        "dp_id": 141,
        "code": "set_silent_speed",
        "name": "Silent Mode Fan Speed",
        "icon": "mdi:fan",
        "unit": "RPM",
        "min_value": 300.0,
        "max_value": 700.0,
        "step": 10.0,
        "api_conversion": "int(value)",
    },
}

# ====================================================
# SELECT TYPES
# ====================================================
SELECT_TYPES = {
    "mode": {
        "dp_id": 2,
        "code": "mode",
        "name": "Mode",
        "icon": "mdi:hvac",
        "options": {
            "cold": "Cooling",
            "heating": "Heating",
        },
    },
    "work_mode": {
        "dp_id": 5,
        "code": "work_mode",
        "name": "Work Mode",
        "icon": "mdi:cog",
        "options": {
            "smart": "Smart",
            "silent": "Silent",
        },
    },
}
