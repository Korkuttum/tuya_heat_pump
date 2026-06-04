"""Model mapping for WOPOLTOP Heat Pump (enhs6o)."""

MODEL_NAME = "WOPOLTOP Heat Pump (enhs6o)"
# ====================================================
# Wopoltop @goofee76
# ====================================================
SENSOR_TYPES = {
    # Current Temperature (dp_id: 3)
    "temp_current": {
        "dp_id": 3,
        "code": "temp_current",
        "name": "Current Temperature",
        "unit": "°F",
        "icon": "mdi:thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
    },
}

# ====================================================
# BINARY SENSOR TYPES (read-only bitmap - accessMode: "ro")
# ====================================================
BINARY_SENSOR_TYPES = {
    # Fault Alarm - Bitmap (dp_id: 6)
    "fault": {
        "dp_id": 6,
        "code": "fault",
        "name": "Fault Alarm",
        "device_class": "problem",
        "conversion": "value != 0",
    },
}

# ====================================================
# SWITCH TYPES (read-write bool - accessMode: "rw")
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
}

# ====================================================
# NUMBER TYPES (read-write value - accessMode: "rw")
# ====================================================
NUMBER_TYPES = {
    # Target Temperature Setpoint (dp_id: 2)
    "temp_set": {
        "dp_id": 2,
        "code": "temp_set",
        "name": "Target Temperature",
        "icon": "mdi:thermostat",
        "unit": "°F",
        "min_value": 46.0,
        "max_value": 104.0,
        "step": 1.0,
        "api_conversion": "value",
    },
}

# ====================================================
# SELECT TYPES (read-write enum - accessMode: "rw")
# ====================================================
SELECT_TYPES = {
    # Operating Mode (dp_id: 4) - hot, cold, auto, eco
    "mode": {
        "dp_id": 4,
        "code": "mode",
        "name": "Working Mode",
        "icon": "mdi:hvac",
        "options": {
            "hot": "Heating",
            "cold": "Cooling",
            "auto": "Auto",
            "eco": "ECO",
        },
    },
}
