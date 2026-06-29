"""Model mapping for Tuya Inverter Pool Heat Pump (modelId: 0000000tqc)."""

MODEL_NAME = "Tuya Inverter Pool Heat Pump (0000000tqc)"
# ====================================================
#  Fairland Inverter Plus @latecka
# ====================================================
SENSOR_TYPES = {
    # Temperature Sensors
    "WInTemp": {
        "dp_id": 102,
        "code": "WInTemp",
        "name": "Water Inlet Temperature",
        "unit": "°C",
        "icon": "mdi:pool-thermometer",
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
    "OutPipeTemp": {
        "dp_id": 120,
        "code": "OutPipeTemp",
        "name": "Outdoor Coil Temperature",
        "unit": "°C",
        "icon": "mdi:thermometer-lines",
        "device_class": "temperature",
        "state_class": "measurement",
    },
    "ExhaustTemp": {
        "dp_id": 122,
        "code": "ExhaustTemp",
        "name": "Discharge Temperature",
        "unit": "°C",
        "icon": "mdi:thermometer-alert",
        "device_class": "temperature",
        "state_class": "measurement",
    },
    "RadTemp": {
        "dp_id": 127,
        "code": "RadTemp",
        "name": "Heatsink Temperature",
        "unit": "°C",
        "icon": "mdi:thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
    },

    # Setpoint Limits (read-only, from device)
    "SetDnLimit": {
        "dp_id": 107,
        "code": "SetDnLimit",
        "name": "Setpoint Lower Limit",
        "unit": "°C",
        "icon": "mdi:thermometer-low",
        "device_class": "temperature",
        "state_class": "measurement",
    },
    "SetUpLimit": {
        "dp_id": 108,
        "code": "SetUpLimit",
        "name": "Setpoint Upper Limit",
        "unit": "°C",
        "icon": "mdi:thermometer-high",
        "device_class": "temperature",
        "state_class": "measurement",
    },

    # Compressor & Performance
    "CompFreAct": {
        "dp_id": 125,
        "code": "CompFreAct",
        "name": "Compressor Frequency",
        "unit": "Hz",
        "icon": "mdi:cosine-wave",
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
    "SpeedPercentage": {
        "dp_id": 104,
        "code": "SpeedPercentage",
        "name": "Compressor Speed",
        "unit": "%",
        "icon": "mdi:speedometer",
        "state_class": "measurement",
    },

    # Mechanical positions
    "EXVPosition": {
        "dp_id": 128,
        "code": "EXVPosition",
        "name": "Electronic Expansion Valve Position",
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

    # AC Fan Speed (read-only enum, exposed as text sensor)
    "ACFanSpeed": {
        "dp_id": 140,
        "code": "ACFanSpeed",
        "name": "AC Fan Speed",
        "icon": "mdi:fan",
        "conversion": "{'LowSpeed': 'Low', 'MidSpeed': 'Medium', 'HighSpeed': 'High', 'STOP': 'Stop'}.get(value, value)"
    },
}

BINARY_SENSOR_TYPES = {
    "WarmOrCool": {
        "dp_id": 118,
        "code": "WarmOrCool",
        "name": "Cooling Active",
        "device_class": "running",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']"
    },
    "Defrost": {
        "dp_id": 130,
        "code": "Defrost",
        "name": "Defrost",
        "device_class": "heat",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']"
    },
    "CompRly": {
        "dp_id": 134,
        "code": "CompRly",
        "name": "Compressor Relay",
        "device_class": "running",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']"
    },
    "CyclePump": {
        "dp_id": 135,
        "code": "CyclePump",
        "name": "Circulation Pump",
        "device_class": "running",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']"
    },
    "ReserveValve": {
        "dp_id": 136,
        "code": "ReserveValve",
        "name": "4-Way Valve",
        "device_class": "opening",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']"
    },
    "ChargeRly": {
        "dp_id": 139,
        "code": "ChargeRly",
        "name": "Soft-Start Relay",
        "device_class": "running",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']"
    },
    "fault1": {
        "dp_id": 115,
        "code": "fault1",
        "name": "Fault Alarm 1",
        "device_class": "problem",
        "conversion": "value != 0"
    },
    "fault2": {
        "dp_id": 116,
        "code": "fault2",
        "name": "Fault Alarm 2",
        "device_class": "problem",
        "conversion": "value != 0"
    },
}

SWITCH_TYPES = {
    "Power": {
        "dp_id": 1,
        "code": "Power",
        "name": "Power",
        "icon": "mdi:power",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']"
    },
    "SilentMdoe": {
        "dp_id": 117,
        "code": "SilentMdoe",
        "name": "Smart Mode (off = Silent)",
        "icon": "mdi:brain",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']"
    },
}

NUMBER_TYPES = {
    "SetTemp": {
        "dp_id": 106,
        "code": "SetTemp",
        "name": "Target Temperature",
        "icon": "mdi:thermometer",
        "unit": "°C",
        # Device enforces narrower ranges per mode: Heat 18-40, Cool 12-30.
        # SetDnLimit (dp 107) and SetUpLimit (dp 108) report the active mode's limits.
        # Static range covers both; device rejects out-of-range values.
        "min_value": 12.0,
        "max_value": 40.0,
        "step": 1.0,
        "conversion": "value",
        "api_conversion": "round(value)"
    },
}

SELECT_TYPES = {
    "SetMode": {
        "dp_id": 105,
        "code": "SetMode",
        "name": "Work Mode",
        "icon": "mdi:air-conditioner",
        "options": {
            "smart": "Auto",
            "warm": "Heat",
            "cool": "Cool"
        },
    },
}
