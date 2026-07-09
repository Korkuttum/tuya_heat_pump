"""Model mapping for Rotenso Heat Pump (modelId: 000004k4z6)."""

MODEL_NAME = "Rotenso Heat Pump (000004k4z6)"
# ====================================================
# Rotenso Heat Pump @tvofi
# modelId: 000004k4z6
# Notes:
#   - Rotenso uses its own internal sensor labeling (Tin, Tout, T3..T9, TL,
#     Tw2, T1B). Tin/Tout are inlet/outlet water; the rest are internal
#     probe positions that vary between models.
#   - Tw2 (dp 114) and T1B (dp 116) return -30°C sentinel when the probe
#     is not wired.
#   - Temperatures use scale=0 (per device model spec, confirmed by user):
#     values are already in °C, no conversion needed.
#   - POWER (dp 108) spec scale=1 (W ÷ 10).
#   - mode options confirmed from device model: cool, heat, DHW, COOLDHW,
#     HEATDHW.
#   - timer (dp 16) is a raw DP that comes without a value field (handled
#     safely by the coordinator).
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
    },
    "temp_current_f": {
        "dp_id": 26,
        "code": "temp_current_f",
        "name": "Current Temperature (°F)",
        "unit": "°F",
        "icon": "mdi:thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
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
    },
    "Tout": {
        "dp_id": 106,
        "code": "Tout",
        "name": "Water Outlet Temperature (Tout)",
        "unit": "°C",
        "icon": "mdi:thermometer-water",
        "device_class": "temperature",
        "state_class": "measurement",
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
    },
    "T4": {
        "dp_id": 105,
        "code": "T4",
        "name": "Sensor T4",
        "unit": "°C",
        "icon": "mdi:thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
    },
    "T5": {
        "dp_id": 111,
        "code": "T5",
        "name": "Sensor T5",
        "unit": "°C",
        "icon": "mdi:thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
    },
    "T6": {
        "dp_id": 107,
        "code": "T6",
        "name": "Sensor T6",
        "unit": "°C",
        "icon": "mdi:thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
    },
    "T9": {
        "dp_id": 113,
        "code": "T9",
        "name": "Sensor T9",
        "unit": "°C",
        "icon": "mdi:thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
    },
    "TL": {
        "dp_id": 112,
        "code": "TL",
        "name": "Sensor TL",
        "unit": "°C",
        "icon": "mdi:thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
    },
    "Tw2": {
        "dp_id": 114,
        "code": "Tw2",
        "name": "Sensor Tw2 (Auxiliary Water)",
        "unit": "°C",
        "icon": "mdi:thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
    },
    "T1B": {
        "dp_id": 116,
        "code": "T1B",
        "name": "Sensor T1B (Auxiliary)",
        "unit": "°C",
        "icon": "mdi:thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
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
NUMBER_TYPES = {
    "temp_set": {
        "dp_id": 9,
        "code": "temp_set",
        "name": "Temperature Setpoint",
        "icon": "mdi:thermostat",
        "unit": "°C",
        "min_value": 5.0,
        "max_value": 65.0,
        "step": 1.0,
        "api_conversion": "int(value)",
    },
    "DHWSET": {
        "dp_id": 104,
        "code": "DHWSET",
        "name": "DHW Setpoint",
        "icon": "mdi:water-thermometer",
        "unit": "°C",
        "min_value": 40.0,
        "max_value": 65.0,
        "step": 1.0,
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
