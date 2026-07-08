"""Model mapping for Rotenso Heat Pump (modelId: 000004k4z6)."""

MODEL_NAME = "Rotenso Heat Pump (000004k4z6)"
# ====================================================
# Rotenso @tvofi
# ====================================================

SENSOR_TYPES = {
    # ---- Main temperatures ----
    "temp_current": {
        "dp_id": 10,
        "code": "temp_current",
        "name": "Current Temperature",
        "unit": "°C",
        "icon": "mdi:thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
        "conversion": "value / 10",
    },
    "temp_current_f": {
        "dp_id": 26,
        "code": "temp_current_f",
        "name": "Current Temperature (°F)",
        "unit": "°F",
        "icon": "mdi:thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
        "conversion": "value / 10",
    },

    # ---- Water loop temperatures ----
    "Tin": {
        "dp_id": 101,
        "code": "Tin",
        "name": "Water Inlet Temperature (Tin)",
        "unit": "°C",
        "icon": "mdi:thermometer-water",
        "device_class": "temperature",
        "state_class": "measurement",
        "conversion": "value / 10",
    },
    "Tout": {
        "dp_id": 106,
        "code": "Tout",
        "name": "Water Outlet Temperature (Tout)",
        "unit": "°C",
        "icon": "mdi:thermometer-water",
        "device_class": "temperature",
        "state_class": "measurement",
        "conversion": "value / 10",
    },

    # ---- Internal probes (Rotenso naming) ----
    "T3": {
        "dp_id": 115,
        "code": "T3",
        "name": "Sensor T3",
        "unit": "°C",
        "icon": "mdi:thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
        "conversion": "value / 10",
    },
    "T4": {
        "dp_id": 105,
        "code": "T4",
        "name": "Sensor T4",
        "unit": "°C",
        "icon": "mdi:thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
        "conversion": "value / 10",
    },
    "T5": {
        "dp_id": 111,
        "code": "T5",
        "name": "Sensor T5",
        "unit": "°C",
        "icon": "mdi:thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
        "conversion": "value / 10",
    },
    "T6": {
        "dp_id": 107,
        "code": "T6",
        "name": "Sensor T6",
        "unit": "°C",
        "icon": "mdi:thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
        "conversion": "value / 10",
    },
    "T9": {
        "dp_id": 113,
        "code": "T9",
        "name": "Sensor T9",
        "unit": "°C",
        "icon": "mdi:thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
        "conversion": "value / 10",
    },
    "TL": {
        "dp_id": 112,
        "code": "TL",
        "name": "Sensor TL",
        "unit": "°C",
        "icon": "mdi:thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
        "conversion": "value / 10",
    },
    "Tw2": {
        "dp_id": 114,
        "code": "Tw2",
        "name": "Sensor Tw2 (Auxiliary Water)",
        "unit": "°C",
        "icon": "mdi:thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
        "conversion": "value / 10",
    },
    "T1B": {
        "dp_id": 116,
        "code": "T1B",
        "name": "Sensor T1B (Auxiliary)",
        "unit": "°C",
        "icon": "mdi:thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
        "conversion": "value / 10",
    },

    # ---- Electrical & pump ----
    "POWER": {
        "dp_id": 108,
        "code": "POWER",
        "name": "Power",
        "unit": "W",
        "icon": "mdi:flash",
        "device_class": "power",
        "state_class": "measurement",
        "conversion": "value / 10",
    },
    "WP_speed": {
        "dp_id": 109,
        "code": "WP_speed",
        "name": "Water Pump Speed",
        "unit": "%",
        "icon": "mdi:water-pump",
        "state_class": "measurement",
    },
}

# ====================================================
# BINARY SENSOR TYPES
# ====================================================
BINARY_SENSOR_TYPES = {
    "fault": {
        "dp_id": 20,
        "code": "fault",
        "name": "Fault Alarm",
        "device_class": "problem",
        "conversion": "value != 0",
    },
    "DEF": {
        "dp_id": 102,
        "code": "DEF",
        "name": "Defrosting",
        "device_class": "cold",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']",
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
    "disinfection": {
        "dp_id": 4,
        "code": "disinfection",
        "name": "Disinfection Mode",
        "icon": "mdi:shield-check",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']",
    },
    "switch_microwave": {
        "dp_id": 7,
        "code": "switch_microwave",
        "name": "Microwave",
        "icon": "mdi:radio-tower",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']",
    },
    "instant_heating": {
        "dp_id": 15,
        "code": "instant_heating",
        "name": "Instant Heating",
        "icon": "mdi:heating-coil",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']",
    },
    "night_mode": {
        "dp_id": 110,
        "code": "night_mode",
        "name": "Night Mode",
        "icon": "mdi:weather-night",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']",
    },
}

# ====================================================
# NUMBER TYPES
# ====================================================
# Range values reflect what the user sees in HA (after /10 conversion).
# api_conversion multiplies by 10 and casts to int before sending to device.
NUMBER_TYPES = {
    "temp_set": {
        "dp_id": 9,
        "code": "temp_set",
        "name": "Temperature Setpoint",
        "icon": "mdi:thermostat",
        "unit": "°C",
        "min_value": 0.5,
        "max_value": 65.0,
        "step": 0.5,
        "conversion": "value / 10",
        "api_conversion": "int(value * 10)",
    },
    "DHWSET": {
        "dp_id": 104,
        "code": "DHWSET",
        "name": "DHW Setpoint",
        "icon": "mdi:water-thermometer",
        "unit": "°C",
        "min_value": 4.0,
        "max_value": 65.0,
        "step": 0.5,
        "conversion": "value / 10",
        "api_conversion": "int(value * 10)",
    },
}

# ====================================================
# SELECT TYPES
# ====================================================
SELECT_TYPES = {
    "mode": {
        "dp_id": 2,
        "code": "mode",
        "name": "Operation Mode",
        "icon": "mdi:hvac",
        "options": {
            "cool": "Cooling",
            "heat": "Heating",
            "DHW": "DHW (Hot Water)",
            "COOLDHW": "Cooling + DHW",
            "HEATDHW": "Heating + DHW",
        },
    },
}
