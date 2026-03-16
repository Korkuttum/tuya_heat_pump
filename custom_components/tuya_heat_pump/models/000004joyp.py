"""Model mapping for 000004joyp (New Heat Pump Model)."""

MODEL_NAME = "Tuya Heat Pump (000004joyp)"

# ====================================================
# SENSOR TYPES - Read-only values from the device
# ====================================================
SENSOR_TYPES = {
    # Inlet Water Temperature (ro)
    "wintemp": {
        "dp_id": 103,
        "code": "wintemp",
        "name": "Inlet Water Temperature",
        "unit": "°C",
        "icon": "mdi:thermometer-water",
        "device_class": "temperature",
        "state_class": "measurement",
        "conversion": "value",  # Scale 0, so direct value
    },
    # Speed Percentage (ro)
    "speedpercentage": {
        "dp_id": 105,
        "code": "speedpercentage",
        "name": "Speed Percentage",
        "unit": "%",
        "icon": "mdi:speedometer",
        "state_class": "measurement",
        "conversion": "value",
    },
    # Temperature Lower Limit (ro)
    "setdnlimit": {
        "dp_id": 108,
        "code": "setdnlimit",
        "name": "Temperature Lower Limit",
        "unit": "°C",
        "icon": "mdi:thermometer-chevron-down",
        "device_class": "temperature",
        "state_class": "measurement",
        "conversion": "value",
    },
    # Temperature Upper Limit (ro)
    "setuplimit": {
        "dp_id": 109,
        "code": "setuplimit",
        "name": "Temperature Upper Limit",
        "unit": "°C",
        "icon": "mdi:thermometer-chevron-up",
        "device_class": "temperature",
        "state_class": "measurement",
        "conversion": "value",
    },
    # Power (ro) - with scale 3 (divide by 1000)
    "rateofwork": {
        "dp_id": 112,
        "code": "rateofwork",
        "name": "Power",
        "unit": "kW",
        "icon": "mdi:flash",
        "device_class": "power",
        "state_class": "measurement",
        "conversion": "value / 1000",  # scale: 3
    },
}

# ====================================================
# BINARY SENSOR TYPES - Read-only boolean/bitmap
# ====================================================
BINARY_SENSOR_TYPES = {
    # Fault 1 (ro) - Bitmap
    "fault1": {
        "dp_id": 110,
        "code": "fault1",
        "name": "Fault Status 1",
        "device_class": "problem",
        "conversion": "value != 0",  # 0 = no fault
    },
    # Fault 2 (ro) - Bitmap
    "fault2": {
        "dp_id": 111,
        "code": "fault2",
        "name": "Fault Status 2",
        "device_class": "problem",
        "conversion": "value != 0",
    },
    # Power Display Enable (ro)
    "enablepowerbit": {
        "dp_id": 113,
        "code": "enablepowerbit",
        "name": "Power Display Enable",
        "icon": "mdi:eye",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']",
    },
}

# ====================================================
# SWITCH TYPES - Read-write boolean
# ====================================================
SWITCH_TYPES = {
    # Power Switch (rw)
    "power": {
        "dp_id": 101,
        "code": "power",
        "name": "Power",
        "icon": "mdi:power",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']",
        "api_conversion": "value",  # Direct boolean
    },
    # Temperature Unit Switch (rw) - 0=Celsius, 1=Fahrenheit
    "change_tem": {
        "dp_id": 104,
        "code": "change_tem",
        "name": "Temperature Unit",
        "icon": "mdi:thermometer",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']",
        "api_conversion": "value",
    },
}

# ====================================================
# NUMBER TYPES - Read-write numeric values
# ====================================================
NUMBER_TYPES = {
    # Temperature Setpoint (rw)
    "settemp": {
        "dp_id": 107,
        "code": "settemp",
        "name": "Target Temperature",
        "icon": "mdi:thermostat",
        "unit": "°C",
        "min_value": -22.0,  # From model spec
        "max_value": 122.0,  # From model spec
        "step": 1.0,
        "conversion": "value",
        "api_conversion": "value",
    },
}

# ====================================================
# SELECT TYPES - Read-write enum
# ====================================================
SELECT_TYPES = {
    # Operation Mode 1 (rw) - silence, smart, booster
    "mode1": {
        "dp_id": 102,
        "code": "mode1",
        "name": "Operation Mode 1",
        "icon": "mdi:hvac",
        "options": {
            "silence": "Silent",
            "smart": "Smart",
            "booster": "Booster",
        },
        "conversion": "value",
        "api_conversion": "value",
    },
    # Operation Mode 2 (rw) - smart, warm, cool
    "setmode": {
        "dp_id": 106,
        "code": "setmode",
        "name": "Operation Mode 2",
        "icon": "mdi:air-conditioner",
        "options": {
            "smart": "Smart",
            "warm": "Warm",
            "cool": "Cool",
        },
        "conversion": "value",
        "api_conversion": "value",
    },
    # Cooling Enable (ro) - 0 or 1
    "cool_en": {
        "dp_id": 114,
        "code": "cool_en",
        "name": "Cooling Enable",
        "icon": "mdi:snowflake",
        "options": {
            "0": "Disabled",
            "1": "Enabled",
        },
        "conversion": "value",
        "api_conversion": "value",
    },
    # Booster Enable (ro) - 0 or 1
    "booster_en": {
        "dp_id": 115,
        "code": "booster_en",
        "name": "Booster Enable",
        "icon": "mdi:rocket-launch",
        "options": {
            "0": "Disabled",
            "1": "Enabled",
        },
        "conversion": "value",
        "api_conversion": "value",
    },
}
