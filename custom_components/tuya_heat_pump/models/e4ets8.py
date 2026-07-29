"""Model mapping for the AMT-Pool Mini heat pump (e4ets8)."""

MODEL_NAME = "AMT-Pool Mini"

SENSOR_TYPES = {
    "temp_current": {
        "dp_id": 3,
        "code": "temp_current",
        "name": "Current Temperature",
        "unit": "°C",
        "icon": "mdi:thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
    },
    "fault": {
        "dp_id": 13,
        "code": "fault",
        "name": "Fault Code",
        "icon": "mdi:alert-circle",
        "conversion": "value",
    },
}

BINARY_SENSOR_TYPES = {
    "fault": {
        "dp_id": 13,
        "code": "fault",
        "name": "Fault",
        "device_class": "problem",
        "conversion": "value != 0",
    },
}

SWITCH_TYPES = {
    "switch": {
        "dp_id": 1,
        "code": "switch",
        "name": "Power",
        "icon": "mdi:power",
        "conversion": "value in [1, True, '1', 'true', 'on']",
    },
}

NUMBER_TYPES = {
    "temp_set": {
        "dp_id": 2,
        "code": "temp_set",
        "name": "Target Temperature",
        "icon": "mdi:thermostat",
        "unit": "°C",
        "min_value": 0,
        "max_value": 40,
        "step": 1,
        "api_conversion": "value",
    },
}

SELECT_TYPES = {
    "mode": {
        "dp_id": 4,
        "code": "mode",
        "name": "Operating Mode",
        "icon": "mdi:hvac",
        "options": {
            "Heat": "Heating",
            "Cool": "Cooling",
            "Auto": "Automatic",
        },
    },
}
