"""Model mapping for Heat Pump (fc1fls)."""

MODEL_NAME = "Heat Pump (fc1fls)"
# ====================================================
# Power World R290 @brownnath2000
# ====================================================
SENSOR_TYPES = {
    # ========== FAULT & STATUS ==========
    "custom_fault_bit": {
        "dp_id": 199,
        "code": "custom_fault_bit",
        "name": "Custom Fault",
        "icon": "mdi:alert-circle",
        "device_class": "problem",
        "state_class": "measurement",
    },
    "products_id": {
        "dp_id": 180,
        "code": "products_id",
        "name": "Product ID",
        "icon": "mdi:identifier",
    },
}

# ====================================================
# BINARY SENSOR TYPES (read-only bool/bitmap - accessMode: "ro")
# ====================================================
BINARY_SENSOR_TYPES = {
    "fault": {
        "dp_id": 15,
        "code": "fault",
        "name": "Fault Alarm",
        "icon": "mdi:alert-circle",
        "device_class": "problem",
        "conversion": "value != 0"
    },
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
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']"
    },
    "reset": {
        "dp_id": 125,
        "code": "reset",
        "name": "Reset to Default",
        "icon": "mdi:restore",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']"
    },
}

# ====================================================
# NUMBER TYPES (read-write value - accessMode: "rw")
# ====================================================
NUMBER_TYPES = {
    "hot_water_set": {
        "dp_id": 110,
        "code": "hot_water_set",
        "name": "Hot Water Temperature Setpoint",
        "icon": "mdi:water-thermometer",
        "unit": "°C",
        "min_value": 0.0,
        "max_value": 99.0,
        "step": 1.0,
        "api_conversion": "value"
    },
    "heating_setting": {
        "dp_id": 111,
        "code": "heating_setting",
        "name": "Heating Temperature Setpoint",
        "icon": "mdi:thermostat",
        "unit": "°C",
        "min_value": 0.0,
        "max_value": 99.0,
        "step": 1.0,
        "api_conversion": "value"
    },
    "cooling_setting": {
        "dp_id": 112,
        "code": "cooling_setting",
        "name": "Cooling Temperature Setpoint",
        "icon": "mdi:snowflake",
        "unit": "°C",
        "min_value": 0.0,
        "max_value": 99.0,
        "step": 1.0,
        "api_conversion": "value"
    },
    "hdef": {
        "dp_id": 130,
        "code": "hdef",
        "name": "Force Defrost",
        "icon": "mdi:snowflake-melt",
        "unit": "",
        "min_value": 1.0,
        "max_value": 8.0,
        "step": 1.0,
        "api_conversion": "value"
    },
}

# ====================================================
# SELECT TYPES (read-write enum - accessMode: "rw")
# ====================================================
SELECT_TYPES = {
    "mode": {
        "dp_id": 2,
        "code": "mode",
        "name": "Frequency Mode",
        "icon": "mdi:sine-wave",
        "options": {
            "smart": "Smart",
            "strong": "Strong",
            "mute": "Mute"
        },
    },
    "work_mode": {
        "dp_id": 5,
        "code": "work_mode",
        "name": "Operation Mode",
        "icon": "mdi:hvac",
        "options": {
            "wth": "Hot Water",
            "heat": "Heating",
            "cool": "Cooling",
            "wth_heat": "Hot Water + Heating",
            "wth_cool": "Hot Water + Cooling"
        },
    },
    "temp_unit_convert": {
        "dp_id": 6,
        "code": "temp_unit_convert",
        "name": "Temperature Unit",
        "icon": "mdi:thermometer",
        "options": {
            "c": "Celsius",
            "f": "Fahrenheit"
        },
    },
}
