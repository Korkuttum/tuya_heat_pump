"""Model mapping for Aquark Heat Pump (000000324z)."""

MODEL_NAME = "Aquark Heat Pump (000000324z)"
# ====================================================
# Aquark @reitermarkus
# ====================================================
SENSOR_TYPES = {
    "WInTemp": {
        "dp_id": 102,
        "code": "WInTemp",
        "name": "Inlet Water Temperature",
        "unit": "°C",
        "icon": "mdi:thermometer-water",
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
    "SetDnLimit": {
        "dp_id": 107,
        "code": "SetDnLimit",
        "name": "Temperature Lower Limit",
        "unit": "°C",
        "icon": "mdi:thermometer-chevron-down",
        "device_class": "temperature",
        "state_class": "measurement",
    },
    "SetUpLimit": {
        "dp_id": 108,
        "code": "SetUpLimit",
        "name": "Temperature Upper Limit",
        "unit": "°C",
        "icon": "mdi:thermometer-chevron-up",
        "device_class": "temperature",
        "state_class": "measurement",
    },
    "OutPipeTemp": {
        "dp_id": 120,
        "code": "OutPipeTemp",
        "name": "Outdoor Coil Temperature",
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
        "icon": "mdi:thermometer-alert",
        "device_class": "temperature",
        "state_class": "measurement",
    },
    "AmbTemp": {
        "dp_id": 124,
        "code": "AmbTemp",
        "name": "Ambient Temperature",
        "unit": "°C",
        "icon": "mdi:home-thermometer",
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
    "RadTemp": {
        "dp_id": 127,
        "code": "RadTemp",
        "name": "Radiator Temperature",
        "unit": "°C",
        "icon": "mdi:thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
    },
    "EXVPosition": {
        "dp_id": 128,
        "code": "EXVPosition",
        "name": "Electronic Expansion Valve Opening",
        "unit": "P",
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
    # ========== SETPOINTS (read-only for display) ==========
    "SetTemp": {
        "dp_id": 106,
        "code": "SetTemp",
        "name": "Temperature Setpoint",
        "unit": "°C",
        "icon": "mdi:thermostat",
        "device_class": "temperature",
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
        "name": "Fault Code 1",
        "icon": "mdi:alert-circle",
        "device_class": "problem",
        "conversion": "value != 0",
    },
    "fault2": {
        "dp_id": 116,
        "code": "fault2",
        "name": "Fault Code 2",
        "icon": "mdi:alert-circle",
        "device_class": "problem",
        "conversion": "value != 0",
    },
    "WarmOrCool": {
        "dp_id": 118,
        "code": "WarmOrCool",
        "name": "Heating or Cooling Mode",
        "icon": "mdi:hvac",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']",
        "options": {
            False: "Heating",
            True: "Cooling",
        },
    },
    "Defrost": {
        "dp_id": 130,
        "code": "Defrost",
        "name": "Defrost Status",
        "icon": "mdi:snowflake-melt",
        "device_class": "cold",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']",
    },
    "CompRly": {
        "dp_id": 134,
        "code": "CompRly",
        "name": "Compressor Contactor",
        "icon": "mdi:engine",
        "device_class": "running",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']",
    },
    "CyclePump": {
        "dp_id": 135,
        "code": "CyclePump",
        "name": "Circulation Pump",
        "icon": "mdi:water-pump",
        "device_class": "running",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']",
    },
    "ReserveValve": {
        "dp_id": 136,
        "code": "ReserveValve",
        "name": "Four-Way Valve",
        "icon": "mdi:valve",
        "device_class": "opening",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']",
    },
    "ChargeRly": {
        "dp_id": 139,
        "code": "ChargeRly",
        "name": "Charge Relay",
        "icon": "mdi:flash",
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
    "change_tem": {
        "dp_id": 103,
        "code": "change_tem",
        "name": "Temperature Unit",
        "icon": "mdi:thermometer",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']",
        "options": {
            False: "Celsius",
            True: "Fahrenheit",
        },
    },
    "SilentMdoe": {
        "dp_id": 117,
        "code": "SilentMdoe",
        "name": "Silent Mode",
        "icon": "mdi:volume-off",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']",
    },
}

# ====================================================
# NUMBER TYPES (read-write value - accessMode: "rw")
# ====================================================
NUMBER_TYPES = {
    "SetTemp": {
        "dp_id": 106,
        "code": "SetTemp",
        "name": "Temperature Setpoint",
        "icon": "mdi:thermostat",
        "unit": "°C",
        "min_value": -22.0,
        "max_value": 104.0,
        "step": 1.0,
        "api_conversion": "value"
    },
}

# ====================================================
# SELECT TYPES (read-write enum - accessMode: "rw")
# ====================================================
SELECT_TYPES = {
    "SetMode": {
        "dp_id": 105,
        "code": "SetMode",
        "name": "Mode",
        "icon": "mdi:hvac",
        "options": {
            "smart": "Auto",
            "warm": "Heating",
            "cool": "Cooling",
        },
    },
    "ACFanSpeed": {
        "dp_id": 140,
        "code": "ACFanSpeed",
        "name": "AC Fan Speed",
        "icon": "mdi:fan",
        "options": {
            "LowSpeed": "Low Speed",
            "MidSpeed": "Mid Speed",
            "HighSpeed": "High Speed",
        },
    },
}
