"""Model mapping for 000003jtyb (simple heat pump model)."""

MODEL_NAME = "Heat Pump Model 000003jtyb"

# Sensor Types - read-only value types
SENSOR_TYPES = {
    "temp_current": {
        "dp_id": 3,
        "code": "temp_current",
        "name": "Current Temperature",
        "unit": "°C",
        "icon": "mdi:thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
        "conversion": "value"  # Direkt °C
    },
}

# Binary Sensor Types - read-only bool/bitmap
BINARY_SENSOR_TYPES = {
    "fault": {
        "dp_id": 21,
        "code": "fault",
        "name": "Fault Alarm",
        "device_class": "problem",
        "conversion": "value != 0"  # bitmap, 0 ise fault yok
    },
}

# Switch Types - read-write bool
SWITCH_TYPES = {
    "switch": {
        "dp_id": 1,
        "code": "switch",
        "name": "Power",
        "icon": "mdi:power",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']"
    },
}

# Number Types - read-write value
NUMBER_TYPES = {
    "temp_set": {
        "dp_id": 2,
        "code": "temp_set",
        "name": "Target Temperature",
        "icon": "mdi:thermometer",
        "unit": "°C",
        "min_value": 5.0,
        "max_value": 80.0,
        "step": 1.0,
        "conversion": "value",
        "api_conversion": "value"
    },
}

# Select Types - read-write enum
SELECT_TYPES = {
    "mode": {
        "dp_id": 4,
        "code": "mode",
        "name": "Working Mode",
        "icon": "mdi:air-conditioner",
        "options": {
            "auto": "Auto",
            "boost_heat": "Boost Heat",
            "boost_cool": "Boost Cool",
            "eco_heat": "ECO Heat",
            "eco_cool": "ECO Cool",
            "silent_heat": "Silent Heat",
            "silent_cool": "Silent Cool"
        },
        "conversion": "value"
    },
    "freq": {
        "dp_id": 101,
        "code": "freq",
        "name": "Frequency",
        "icon": "mdi:sine-wave",
        "options": {
            "silent": "Silent",
            "normal": "Normal",
            "strong": "Strong"
        },
        "conversion": "value"
    },
}
