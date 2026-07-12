"""Model mapping for Heat Pump (e1kugiu4)."""

MODEL_NAME = "Heat Pump (e1kugiu4)"
# ====================================================
# Mango @Schneider006
# ====================================================

# ====================================================
# SENSOR TYPES (read-only value - accessMode: "ro")
# ====================================================
SENSOR_TYPES = {
    # Current Temperature (dp_id: 24) - scale: 1 (value / 10)
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
    # Hot Water Current Temperature (dp_id: 123) - scale: 1 (value / 10)
    "inlet_temp": {
        "dp_id": 123,
        "code": "inlet_temp",
        "name": "Hot Water Temperature",
        "unit": "°C",
        "icon": "mdi:thermometer-water",
        "device_class": "temperature",
        "state_class": "measurement",
        "conversion": "value / 10",
    },
    # Microcode Version (dp_id: 130) - string
    "r_130": {
        "dp_id": 130,
        "code": "r_130",
        "name": "Microcode Version",
        "icon": "mdi:chip",
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
    # Target Temperature Setpoint (dp_id: 16)
    "temp_set": {
        "dp_id": 16,
        "code": "temp_set",
        "name": "Target Temperature",
        "icon": "mdi:thermostat",
        "unit": "°C",
        "min_value": -10.0,
        "max_value": 85.0,
        "step": 1.0,
        "api_conversion": "value",
    },
    # Hot Water Target Temperature Setpoint (dp_id: 124)
    "temp_set_1": {
        "dp_id": 124,
        "code": "temp_set_1",
        "name": "Hot Water Target Temperature",
        "icon": "mdi:water-thermometer",
        "unit": "°C",
        "min_value": -10.0,
        "max_value": 85.0,
        "step": 1.0,
        "api_conversion": "value",
    },
}

# ====================================================
# SELECT TYPES (read-write enum - accessMode: "rw")
# ====================================================
SELECT_TYPES = {
    # Mode (dp_id: 2) - auto, cold, hot, dhw, cold_dhw, hot_dhw
    "mode": {
        "dp_id": 2,
        "code": "mode",
        "name": "Mode",
        "icon": "mdi:hvac",
        "options": {
            "auto": "Auto",
            "cold": "Cooling",
            "hot": "Heating",
            "dhw": "Hot Water",
            "cold_dhw": "Cooling + Hot Water",
            "hot_dhw": "Heating + Hot Water",
        },
    },
}
NUMBER_TYPES = globals().get("NUMBER_TYPES", {})
NUMBER_TYPES.update({
    "invtttemp": {
        "dp_id": 135,
        "code": "invtttemp",
        "raw_source": "r_135",
        "field_index": 41,
        "encoding": "int32_be",
        "conversion": "value / 10",
        "api_conversion": "value * 10",
        "step": 1,
        "name": "INVT Temperature",
        "unit": "°C",
        "icon": "mdi:thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
    },
    "input_voltage_frequency_conversion": {
        "dp_id": 135,
        "code": "input_voltage_frequency_conversion",
        "raw_source": "r_135",
        "field_index": 48,
        "encoding": "int32_be",
        "conversion": "value / 10",
        "api_conversion": "value * 10",
        "step": 1,
        "name": "Input Voltage (Frequency Conversion)",
        "unit": "V",
        "icon": "mdi:lightning-bolt",
        "device_class": "voltage",
        "state_class": "measurement",
    },
    "ambient_temperature_2": {
        "dp_id": 140,
        "code": "ambient_temperature_2",
        "raw_source": "r_140",
        "field_index": 32,
        "encoding": "int32_be",
        "conversion": "value / 10000",
        "api_conversion": "value * 10000",
        "step": 1,
        "name": "Ambient Temperature?",
        "unit": "°C",
        "icon": "mdi:thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
    },
})
