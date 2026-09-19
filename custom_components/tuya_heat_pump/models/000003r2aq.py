"""Model mapping for Aqua Clear Turbo Silence AXR13 Heat Pump (000003r2aq)."""

MODEL_NAME = "Aqua Clear Turbo Silence AXR13 Heat Pump (000003r2aq)"
# ====================================================
# Aqua Clear Turbo Silence AXR13 @danww
# ====================================================
# This device's category ("rs") only registers switch/mode as standard
# functions — every other DP is raw/custom and doesn't appear in the
# category-level instruction set, so the full schema (accessMode, enum
# ranges, scale) was confirmed via the official
# /v2.0/cloud/thing/{device_id}/model endpoint instead (same call
# tuya_api_test.py makes).
#
# Confirmed enum ranges: mode (dp 2) = silence/smart/booster (Smart Life
# labels the third option "Turbo", raw value is "booster"); SetMode
# (dp 105) = smart/warm/cool — this unit's firmware allows a cool mode
# the Smart Life app never surfaces (untested — unknown if this specific
# physical unit has the hardware for it); ACFanSpeed (dp 140) =
# LowSpeed/MidSpeed/HighSpeed.
#
# SetDnLimit (107), SetUpLimit (108) and SpeedPercentage (104) are
# accessMode "ro" per the schema — read-only sensors, not adjustable
# numbers. change_tem (103) is "rw" and is a Celsius/Fahrenheit display
# toggle, not a passive flag — a switch. Rateofwork (142) has scale: 3
# in the schema, so its conversion divides by 1000 for real kW.
#
# No "Holiday Mode" DP exists on this device — intentionally not mapped.

SENSOR_TYPES = {
    "WInTemp": {
        "dp_id": 102,
        "code": "WInTemp",
        "name": "Water In Temperature",
        "unit": "°C",
        "icon": "mdi:thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
    },
    "OutPipeTemp": {
        "dp_id": 120,
        "code": "OutPipeTemp",
        "name": "Outlet Pipe Temperature",
        "unit": "°C",
        "icon": "mdi:thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
    },
    "ExhaustTemp": {
        "dp_id": 122,
        "code": "ExhaustTemp",
        "name": "Exhaust Temperature",
        "unit": "°C",
        "icon": "mdi:thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
    },
    "AmbTemp": {
        "dp_id": 124,
        "code": "AmbTemp",
        "name": "Ambient Temperature",
        "unit": "°C",
        "icon": "mdi:thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
    },
    "RadTemp": {
        "dp_id": 127,
        "code": "RadTemp",
        "name": "Radiator Temperature",
        "unit": "°C",
        "icon": "mdi:thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
    },
    "CompFreAct": {
        "dp_id": 125,
        "code": "CompFreAct",
        "name": "Compressor Frequency",
        "unit": "Hz",
        "icon": "mdi:sine-wave",
        "state_class": "measurement",
    },
    "CompressorCurrent": {
        "dp_id": 126,
        "code": "CompressorCurrent",
        "name": "Compressor Current",
        "unit": "A",
        "icon": "mdi:current-ac",
        "device_class": "current",
        "state_class": "measurement",
    },
    "EXVPosition": {
        "dp_id": 128,
        "code": "EXVPosition",
        "name": "EXV Position",
        "unit": "step",
        "icon": "mdi:pipe-valve",
        "state_class": "measurement",
    },
    "DCFanSpeed": {
        "dp_id": 129,
        "code": "DCFanSpeed",
        "name": "DC Fan Speed",
        "unit": "RPM",
        "icon": "mdi:fan",
        "state_class": "measurement",
    },
    "Rateofwork": {
        "dp_id": 142,
        "code": "Rateofwork",
        "name": "Rate of Work",
        "unit": "kW",
        "icon": "mdi:gauge",
        "device_class": "power",
        "state_class": "measurement",
        "conversion": "value / 1000",
    },
    "SetDnLimit": {
        "dp_id": 107,
        "code": "SetDnLimit",
        "name": "Lower Temperature Limit",
        "unit": "°C",
        "icon": "mdi:thermometer-chevron-down",
        "device_class": "temperature",
        "state_class": "measurement",
    },
    "SetUpLimit": {
        "dp_id": 108,
        "code": "SetUpLimit",
        "name": "Upper Temperature Limit",
        "unit": "°C",
        "icon": "mdi:thermometer-chevron-up",
        "device_class": "temperature",
        "state_class": "measurement",
    },
    "SpeedPercentage": {
        "dp_id": 104,
        "code": "SpeedPercentage",
        "name": "Speed Percentage",
        "unit": "%",
        "icon": "mdi:speedometer",
        "state_class": "measurement",
    },
}

# ====================================================
# BINARY SENSOR TYPES (read-only bool/bitmap - accessMode: "ro")
# ====================================================
BINARY_SENSOR_TYPES = {
    "fault1": {
        "dp_id": 115,
        "code": "fault1",
        "name": "Fault 1",
        "device_class": "problem",
        "conversion": "value not in [0, False, '0', 'false', None]",
    },
    "fault2": {
        "dp_id": 116,
        "code": "fault2",
        "name": "Fault 2",
        "device_class": "problem",
        "conversion": "value not in [0, False, '0', 'false', None]",
    },
    "Defrost": {
        "dp_id": 130,
        "code": "Defrost",
        "name": "Defrost Active",
        "device_class": "heat",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']",
    },
    "CompRly": {
        "dp_id": 134,
        "code": "CompRly",
        "name": "Compressor Relay",
        "device_class": "running",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']",
    },
    "CyclePump": {
        "dp_id": 135,
        "code": "CyclePump",
        "name": "Cycle Pump",
        "device_class": "running",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']",
    },
    "ReserveValve": {
        "dp_id": 136,
        "code": "ReserveValve",
        "name": "Reserve Valve",
        "device_class": "opening",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']",
    },
    "ChargeRly": {
        "dp_id": 139,
        "code": "ChargeRly",
        "name": "Charge Relay",
        "device_class": "running",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']",
    },
    "EnablePowerBit": {
        "dp_id": 143,
        "code": "EnablePowerBit",
        "name": "Power Enabled",
        "device_class": "power",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']",
    },
    "WarmOrCool": {
        "dp_id": 118,
        "code": "WarmOrCool",
        "name": "Warm/Cool Flag",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']",
    },
}

# ====================================================
# SWITCH TYPES (read-write bool - accessMode: "rw")
# ====================================================
SWITCH_TYPES = {
    "Power": {
        "dp_id": 1,
        "code": "Power",
        "name": "Power",
        "icon": "mdi:power",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']",
    },
    "SilentMdoe": {
        "dp_id": 117,
        "code": "SilentMdoe",
        "name": "Mute",
        "icon": "mdi:volume-off",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']",
    },
    # Celsius/Fahrenheit display toggle (dp_id: 103) - 0=C, 1=F.
    "change_tem": {
        "dp_id": 103,
        "code": "change_tem",
        "name": "Fahrenheit Display",
        "icon": "mdi:temperature-fahrenheit",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']",
    },
    # No Holiday Mode DP exists on this device - intentionally not mapped.
}

# ====================================================
# NUMBER TYPES (read-write value - accessMode: "rw")
# ====================================================
NUMBER_TYPES = {
    "SetTemp": {
        "dp_id": 106,
        "code": "SetTemp",
        "name": "Target Temperature",
        "icon": "mdi:thermometer",
        "unit": "°C",
        "min_value": 5.0,
        "max_value": 45.0,
        "step": 1.0,
    },
}

# ====================================================
# SELECT TYPES (read-write enum - accessMode: "rw")
# ====================================================
SELECT_TYPES = {
    "mode": {
        "dp_id": 2,
        "code": "mode",
        "name": "Mode",
        "icon": "mdi:tune",
        "options": {
            "silence": "Silence",
            "smart": "Smart",
            "booster": "Turbo",
        },
    },
    "SetMode": {
        "dp_id": 105,
        "code": "SetMode",
        "name": "Heat/Cool Mode",
        "icon": "mdi:sun-snowflake-variant",
        "options": {
            "smart": "Auto",
            "warm": "Heat",
            "cool": "Cool",
        },
    },
    "ACFanSpeed": {
        "dp_id": 140,
        "code": "ACFanSpeed",
        "name": "AC Fan Speed",
        "icon": "mdi:fan",
        "options": {
            "LowSpeed": "Low",
            "MidSpeed": "Mid",
            "HighSpeed": "High",
        },
    },
}
