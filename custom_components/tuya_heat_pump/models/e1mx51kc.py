"""Model mapping for GRAT GTMF-B30Y Heat Pump (e1mx51kc)."""

MODEL_NAME = "GRAT GTMF-B30Y Heat Pump (e1mx51kc)"
# ====================================================
# GRAT GTMF-B30Y (Sichuan Great Technology, 1.5HP Ice Bath Chiller /
# Heat Pump) @spalacioh
#
# Schema pulled directly from Tuya's own model API (tuya_api_test.py
# output, issue #81) — all plain DPs, no raw payloads. Tuya gave no
# real descriptions for the fault bitmap (just generic "fault_bit0"
# .."fault_bit29" labels), so only the raw value + an any-fault
# binary sensor are exposed, same as other models with an undocumented
# fault bitmap.
# ====================================================

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
    "temp_current_f": {
        "dp_id": 15,
        "code": "temp_current_f",
        "name": "Current Temperature (°F)",
        "unit": "°F",
        "icon": "mdi:thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
    },
    "fault_code": {
        "dp_id": 21,
        "code": "fault_code",
        "name": "Fault Code",
        "icon": "mdi:alert-circle",
        "device_class": "problem",
        "state_class": "measurement",
    },
}

# ====================================================
# BINARY SENSOR TYPES (read-only bool/bitmap - accessMode: "ro")
# ====================================================
BINARY_SENSOR_TYPES = {
    "fault": {
        "dp_id": 21,
        "code": "fault",
        "name": "Fault Alarm",
        "icon": "mdi:alert-circle",
        "device_class": "problem",
        "conversion": "value != 0",
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
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']",
    },
}

# ====================================================
# NUMBER TYPES (read-write value - accessMode: "rw")
# ====================================================
NUMBER_TYPES = {
    "temp_set": {
        "dp_id": 2,
        "code": "temp_set",
        "name": "Temperature Setpoint",
        "icon": "mdi:thermostat",
        "unit": "°C",
        "min_value": 0.0,
        "max_value": 60.0,
        "step": 1.0,
        "api_conversion": "value",
    },
    "temp_set_f": {
        "dp_id": 14,
        "code": "temp_set_f",
        "name": "Temperature Setpoint (°F)",
        "icon": "mdi:thermostat",
        "unit": "°F",
        "min_value": 32.0,
        "max_value": 104.0,
        "step": 1.0,
        "api_conversion": "value",
    },
}

# ====================================================
# SELECT TYPES (read-write enum - accessMode: "rw")
# ====================================================
SELECT_TYPES = {
    "mode": {
        "dp_id": 4,
        "code": "mode",
        "name": "Mode",
        "icon": "mdi:hvac",
        "options": {
            "Heat": "Heating",
            "Cool": "Cooling",
            "Auto": "Auto",
        },
    },
    "temp_unit_convert": {
        "dp_id": 13,
        "code": "temp_unit_convert",
        "name": "Temperature Unit",
        "icon": "mdi:thermometer",
        "options": {
            "c": "Celsius",
            "f": "Fahrenheit",
        },
    },
}
