"""Model mapping for 000004joyp (New Heat Pump Model)."""

MODEL_NAME = "Tuya Heat Pump (000004joyp)"
# ====================================================
# EVOHEAT 40T @andrewboller | IPS Pool Systems @KaaNee
# ====================================================
SENSOR_TYPES = {
    # Inlet Water Temperature
    "wintemp": {
        "dp_id": 103,
        "code": "wintemp",
        "name": "Inlet Water Temperature",
        "unit": "°C",
        "icon": "mdi:thermometer-water",
        "device_class": "temperature",
        "state_class": "measurement",
    },
    # Speed Percentage
    "speedpercentage": {
        "dp_id": 105,
        "code": "speedpercentage",
        "name": "Speed Percentage",
        "unit": "%",
        "icon": "mdi:speedometer",
        "state_class": "measurement",
    },
    # Temperature Lower Limit
    "setdnlimit": {
        "dp_id": 108,
        "code": "setdnlimit",
        "name": "Temperature Lower Limit",
        "unit": "°C",
        "icon": "mdi:thermometer-chevron-down",
        "device_class": "temperature",
        "state_class": "measurement",
    },
    # Temperature Upper Limit
    "setuplimit": {
        "dp_id": 109,
        "code": "setuplimit",
        "name": "Temperature Upper Limit",
        "unit": "°C",
        "icon": "mdi:thermometer-chevron-up",
        "device_class": "temperature",
        "state_class": "measurement",
    },
    # Power (with scale 3)
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
    
    # ========== HATA KODU SENSÖRLERİ ==========
    # Fault 1 Code - Sadece hata kodu veya "OK"
    "fault1_code": {
        "dp_id": 110,
        "code": "fault1",
        "name": "Fault Code 1",
        "icon": "mdi:alert-circle",
        "conversion": "'OK' if value == 0 else f'Code: {value}'",
    },
    # Fault 2 Code - Sadece hata kodu veya "OK"
    "fault2_code": {
        "dp_id": 111,
        "code": "fault2",
        "name": "Fault Code 2",
        "icon": "mdi:alert-circle",
        "conversion": "'OK' if value == 0 else f'Code: {value}'",
    },
}

# ====================================================
# BINARY SENSOR TYPES - Hızlı uyarı için
# ====================================================
BINARY_SENSOR_TYPES = {
    # Fault 1 Binary - Arıza var/yok
    "fault1": {
        "dp_id": 110,
        "code": "fault1",
        "name": "Fault Status 1",
        "device_class": "problem",
        "conversion": "value != 0",
    },
    # Fault 2 Binary - Arıza var/yok
    "fault2": {
        "dp_id": 111,
        "code": "fault2",
        "name": "Fault Status 2",
        "device_class": "problem",
        "conversion": "value != 0",
    },
    # Power Display Enable
    "enablepowerbit": {
        "dp_id": 113,
        "code": "enablepowerbit",
        "name": "Power Display Enable",
        "icon": "mdi:eye",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']",
    },
}

# ====================================================
# SWITCH TYPES
# ====================================================
SWITCH_TYPES = {
    # Power Switch
    "power": {
        "dp_id": 101,
        "code": "power",
        "name": "Power",
        "icon": "mdi:power",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']",
        "api_conversion": "value",
    },
    # Temperature Unit (0=Celsius, 1=Fahrenheit)
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
# NUMBER TYPES
# ====================================================
NUMBER_TYPES = {
    # Target Temperature
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
# SELECT TYPES
# ====================================================
SELECT_TYPES = {
    # Operation Mode 1
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
        "api_conversion": "value",
    },
    # Operation Mode 2
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
        "api_conversion": "value",
    },
    # Cooling Enable (read-only)
    "cool_en": {
        "dp_id": 114,
        "code": "cool_en",
        "name": "Cooling Enable",
        "icon": "mdi:snowflake",
        "options": {
            "0": "Disabled",
            "1": "Enabled",
        },
        "api_conversion": "value",
    },
    # Booster Enable (read-only)
    "booster_en": {
        "dp_id": 115,
        "code": "booster_en",
        "name": "Booster Enable",
        "icon": "mdi:rocket-launch",
        "options": {
            "0": "Disabled",
            "1": "Enabled",
        },
        "api_conversion": "value",
    },
}
