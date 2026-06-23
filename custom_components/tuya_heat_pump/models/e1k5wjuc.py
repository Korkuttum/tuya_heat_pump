"""Model mapping for Power World R290 Full DC Heat Pump (e1k5wjuc)."""

MODEL_NAME = "Power World R290 Full DC Heat Pump (e1k5wjuc)"
# ====================================================
# Power World R290 Full DC @tomoo777
# ====================================================

# ====================================================
# SENSOR TYPES (read-only value - accessMode: "ro")
# ====================================================
SENSOR_TYPES = {
    # Product ID (dp_id: 180)
    "products_id": {
        "dp_id": 180,
        "code": "products_id",
        "name": "Product ID",
        "icon": "mdi:identifier",
    },
    # Fault Code - Raw Bitmap Value (dp_id: 15)
    "fault_code": {
        "dp_id": 15,
        "code": "fault_code",
        "name": "Fault Code 1",
        "icon": "mdi:alert-circle",
        "device_class": "problem",
        "state_class": "measurement",
    },
    # Fault 2 - Raw Bitmap Value (dp_id: 198)
    "fault2_code": {
        "dp_id": 198,
        "code": "fault2_code",
        "name": "Fault Code 2",
        "icon": "mdi:alert-circle",
        "device_class": "problem",
        "state_class": "measurement",
    },
    # Custom Fault Bit (dp_id: 199)
    "custom_fault_bit": {
        "dp_id": 199,
        "code": "custom_fault_bit",
        "name": "Driver Fault (Er20)",
        "icon": "mdi:alert-circle",
        "device_class": "problem",
        "state_class": "measurement",
    },
}

# ====================================================
# BINARY SENSOR TYPES (read-only bitmap - accessMode: "ro")
# ====================================================
BINARY_SENSOR_TYPES = {
    # Fault Status (dp_id: 15)
    "fault": {
        "dp_id": 15,
        "code": "fault",
        "name": "Fault Status 1",
        "device_class": "problem",
        "conversion": "value != 0",
    },
    # Fault 2 Status (dp_id: 198)
    "fault2": {
        "dp_id": 198,
        "code": "fault2",
        "name": "Fault Status 2",
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
    # Reset to Default (dp_id: 125) - accessMode: "wr"
    "reset": {
        "dp_id": 125,
        "code": "reset",
        "name": "Reset to Default",
        "icon": "mdi:restore",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']",
    },
}

# ====================================================
# NUMBER TYPES (read-write value - accessMode: "rw")
# ====================================================
NUMBER_TYPES = {
    # Hot Water Temperature Setpoint (dp_id: 110)
    "wth_set": {
        "dp_id": 110,
        "code": "wth_set",
        "name": "Hot Water Temperature",
        "icon": "mdi:water-thermometer",
        "unit": "°C",
        "min_value": 0.0,
        "max_value": 99.0,
        "step": 1.0,
        "api_conversion": "value",
    },
    # Heating Temperature Setpoint (dp_id: 111)
    "heating_set": {
        "dp_id": 111,
        "code": "heating_set",
        "name": "Heating Temperature",
        "icon": "mdi:thermostat",
        "unit": "°C",
        "min_value": 0.0,
        "max_value": 99.0,
        "step": 1.0,
        "api_conversion": "value",
    },
    # Cooling Temperature Setpoint (dp_id: 112)
    "cooling_set": {
        "dp_id": 112,
        "code": "cooling_set",
        "name": "Cooling Temperature",
        "icon": "mdi:snowflake",
        "unit": "°C",
        "min_value": 0.0,
        "max_value": 99.0,
        "step": 1.0,
        "api_conversion": "value",
    },
    # Manual Defrost (dp_id: 130) - accessMode: "wr"
    "hdef": {
        "dp_id": 130,
        "code": "hdef",
        "name": "Manual Defrost",
        "icon": "mdi:snowflake-melt",
        "unit": "",
        "min_value": 1.0,
        "max_value": 8.0,
        "step": 1.0,
        "api_conversion": "value",
    },
}

# ====================================================
# SELECT TYPES (read-write enum - accessMode: "rw")
# ====================================================
SELECT_TYPES = {
    # Operation Mode (dp_id: 2) - smart, strong, mute
    "mode": {
        "dp_id": 2,
        "code": "mode",
        "name": "Operation Mode",
        "icon": "mdi:hvac",
        "options": {
            "smart": "Smart",
            "strong": "Strong",
            "mute": "Mute",
        },
    },
    # Work Mode (dp_id: 5) - wth, heat, cool, wth_heat, wth_cool
    "work_mode": {
        "dp_id": 5,
        "code": "work_mode",
        "name": "Work Mode",
        "icon": "mdi:cog",
        "options": {
            "wth": "Hot Water",
            "heat": "Heating",
            "cool": "Cooling",
            "wth_heat": "Hot Water + Heating",
            "wth_cool": "Hot Water + Cooling",
        },
    },
    # Temperature Unit (dp_id: 6) - c, f
    "temp_unit_convert": {
        "dp_id": 6,
        "code": "temp_unit_convert",
        "name": "Temperature Unit",
        "icon": "mdi:thermometer",
        "options": {
            "c": "Celsius",
            "f": "Fahrenheit",
        },
    },
}
