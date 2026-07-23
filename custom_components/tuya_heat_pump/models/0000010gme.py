"""Model mapping for Smart Thermostat (0000010gme)."""

MODEL_NAME = "Smart Thermostat (0000010gme)"
# ====================================================
# device_id bff12f7a933f4900f8nrcv ("Kombi Termostat")
# MQTT sufficiency test candidate — labels/codes here are already
# straightforward (no Chinese-name mismatches found), unlike several
# other models in this repo.
# ====================================================

SENSOR_TYPES = {
    "temp_current": {
        "dp_id": 24,
        "code": "temp_current",
        "name": "Current Temperature",
        "unit": "°C",
        "icon": "mdi:thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
        "conversion": "value / 10",
    },
}

# ====================================================
# BINARY SENSOR TYPES (read-only bitmap - accessMode: "ro")
# ====================================================
BINARY_SENSOR_TYPES = {
}

# ====================================================
# SWITCH TYPES (read-write bool - accessMode: "rw")
# ====================================================
SWITCH_TYPES = {
    "switch": {
        "dp_id": 1,
        "code": "switch",
        "name": "Power",
        "icon": "mdi:power",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']",
    },
    "factory_reset": {
        "dp_id": 39,
        "code": "factory_reset",
        "name": "Factory Reset",
        "icon": "mdi:restore",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']",
    },
    "child_lock": {
        "dp_id": 40,
        "code": "child_lock",
        "name": "Child Lock",
        "icon": "mdi:lock",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']",
    },
}

# ====================================================
# NUMBER TYPES (read-write value - accessMode: "rw")
# ====================================================
NUMBER_TYPES = {
    "temp_set": {
        "dp_id": 16,
        "code": "temp_set",
        "name": "Target Temperature",
        "icon": "mdi:thermostat",
        "unit": "°C",
        "min_value": 0.0,
        "max_value": 100.0,
        "step": 0.5,
        "conversion": "value / 10",
        "api_conversion": "int(value * 10)",
    },
    "upper_temp": {
        "dp_id": 19,
        "code": "upper_temp",
        "name": "Upper Temperature Limit",
        "icon": "mdi:thermometer-chevron-up",
        "unit": "°C",
        "min_value": 5.0,
        "max_value": 100.0,
        "step": 0.5,
        "conversion": "value / 10",
        "api_conversion": "int(value * 10)",
    },
    "lower_temp": {
        "dp_id": 26,
        "code": "lower_temp",
        "name": "Lower Temperature Limit",
        "icon": "mdi:thermometer-chevron-down",
        "unit": "°C",
        "min_value": 0.0,
        "max_value": 100.0,
        "step": 0.5,
        "conversion": "value / 10",
        "api_conversion": "int(value * 10)",
    },
    "temp_correction": {
        "dp_id": 27,
        "code": "temp_correction",
        "name": "Temperature Correction",
        "icon": "mdi:thermometer-lines",
        "unit": "°C",
        "min_value": -10.0,
        "max_value": 10.0,
        "step": 0.5,
        "conversion": "value / 10",
        "api_conversion": "int(value * 10)",
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
        "icon": "mdi:hvac",
        "options": {
            "manual": "Manual",
            "eco": "Eco",
            "auto": "Auto",
        },
    },
}
