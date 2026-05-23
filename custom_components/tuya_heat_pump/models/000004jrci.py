"""Model mapping for Fairland Heat Pump (000004jrci)."""

MODEL_NAME = "Fairland Heat Pump (000004jrci)"
# ====================================================
# Fairland @bradleewright
# ====================================================

# ====================================================
# SENSOR TYPES (read-only value - accessMode: "ro")
# ====================================================
SENSOR_TYPES = {
    # Inlet Water Temperature (dp_id: 103)
    "wintemp": {
        "dp_id": 103,
        "code": "wintemp",
        "name": "Inlet Water Temperature",
        "unit": "°C",
        "icon": "mdi:thermometer-water",
        "device_class": "temperature",
        "state_class": "measurement",
    },
    # Speed Percentage (dp_id: 105)
    "speedpercentage": {
        "dp_id": 105,
        "code": "speedpercentage",
        "name": "Speed Percentage",
        "unit": "%",
        "icon": "mdi:speedometer",
        "state_class": "measurement",
    },
    # Temperature Lower Limit (dp_id: 108)
    "setdnlimit": {
        "dp_id": 108,
        "code": "setdnlimit",
        "name": "Temperature Lower Limit",
        "unit": "°C",
        "icon": "mdi:thermometer-chevron-down",
        "device_class": "temperature",
        "state_class": "measurement",
    },
    # Temperature Upper Limit (dp_id: 109)
    "setuplimit": {
        "dp_id": 109,
        "code": "setuplimit",
        "name": "Temperature Upper Limit",
        "unit": "°C",
        "icon": "mdi:thermometer-chevron-up",
        "device_class": "temperature",
        "state_class": "measurement",
    },
    # Power (dp_id: 112) - scale: 3 (value / 1000)
    "rateofwork": {
        "dp_id": 112,
        "code": "rateofwork",
        "name": "Power",
        "unit": "kW",
        "icon": "mdi:flash",
        "device_class": "power",
        "state_class": "measurement",
        "conversion": "value / 1000",
    },
}

# ====================================================
# BINARY SENSOR TYPES (read-only bool/bitmap - accessMode: "ro")
# ====================================================
BINARY_SENSOR_TYPES = {
    # Fault 1 - Bitmap (dp_id: 110)
    "fault1": {
        "dp_id": 110,
        "code": "fault1",
        "name": "Fault 1",
        "device_class": "problem",
        "conversion": "value != 0",
    },
    # Fault 2 - Bitmap (dp_id: 111)
    "fault2": {
        "dp_id": 111,
        "code": "fault2",
        "name": "Fault 2",
        "device_class": "problem",
        "conversion": "value != 0",
    },
    # Power Display Enable (dp_id: 113)
    "enablepowerbit": {
        "dp_id": 113,
        "code": "enablepowerbit",
        "name": "Power Display Enable",
        "icon": "mdi:eye",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']",
    },
}

# ====================================================
# SWITCH TYPES (read-write bool - accessMode: "rw")
# ====================================================
SWITCH_TYPES = {
    # Power Switch (dp_id: 101)
    "power": {
        "dp_id": 101,
        "code": "power",
        "name": "Power",
        "icon": "mdi:power",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']",
    },
    # Temperature Unit (dp_id: 104) - False: Celsius, True: Fahrenheit
    "change_tem": {
        "dp_id": 104,
        "code": "change_tem",
        "name": "Temperature Unit",
        "icon": "mdi:thermometer",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']",
        "options": {
            False: "Celsius",
            True: "Fahrenheit",
        },
    },
}

# ====================================================
# NUMBER TYPES (read-write value - accessMode: "rw")
# ====================================================
NUMBER_TYPES = {
    # Target Temperature Setpoint (dp_id: 107)
    "settemp": {
        "dp_id": 107,
        "code": "settemp",
        "name": "Target Temperature",
        "icon": "mdi:thermostat",
        "unit": "°C",
        "min_value": -22.0,
        "max_value": 122.0,
        "step": 1.0,
        "api_conversion": "value",
    },
}

# ====================================================
# SELECT TYPES (read-write enum - accessMode: "rw")
# ====================================================
SELECT_TYPES = {
    # Operation Mode 1 (dp_id: 102) - silence, smart, booster
    "mode1": {
        "dp_id": 102,
        "code": "mode1",
        "name": "Operation Mode",
        "icon": "mdi:hvac",
        "options": {
            "silence": "Silent",
            "smart": "Smart",
            "booster": "Booster",
        },
    },
    # Operation Mode 2 / Selection Mode (dp_id: 106) - smart, warm, cool
    "setmode": {
        "dp_id": 106,
        "code": "setmode",
        "name": "Selection Mode",
        "icon": "mdi:air-conditioner",
        "options": {
            "smart": "Auto",
            "warm": "Heating",
            "cool": "Cooling",
        },
    },
    # Cooling Enable (dp_id: 114) - read-only
    "cool_en": {
        "dp_id": 114,
        "code": "cool_en",
        "name": "Cooling Enable",
        "icon": "mdi:snowflake",
        "options": {
            "0": "Heating Only",
            "1": "Heating & Cooling",
        },
    },
    # Booster Enable (dp_id: 115) - read-only
    "booster_en": {
        "dp_id": 115,
        "code": "booster_en",
        "name": "Booster Enable",
        "icon": "mdi:rocket-launch",
        "options": {
            "0": "Disabled",
            "1": "Enabled",
        },
    },
}
