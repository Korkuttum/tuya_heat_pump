"""Model mapping for Kensol Heat Pump (modelId: fdru4s)."""

MODEL_NAME = "Kensol Heat Pump (fdru4s)"
# ====================================================
# Kensol Heat Pump @VaporX25
# modelId: fdru4s
# DP map sourced from /v2.0/cloud/thing/{id}/shadow/properties + /model
# Notes:
#   - Raw parameter groups (status_pg_1, user_pg_1/2, factory_pg_1/2) are intentionally
#     omitted; they carry base64-encoded blobs with no documented schema.
#   - temp_current (dp 16) reports -30°C sentinel value when the probe is not wired.
#   - fault (dp 15) is a 29-bit bitmap (Er03..Er70). Exposed as a binary "any error" sensor.
#   - fan_module_fault_1/2 (dp 196/197) and custom_fault_bit (dp 199) are integer bitmaps
#     of internal fault registers. Exposed as binary "any error" sensors.
#   - mode (dp 2) is the frequency/behavior profile (smart/strong/mute).
#     work_mode (dp 5) is the actual HVAC mode (heat/cool/auto).
#   - temp_set (dp 4) mirrors the setpoint of the active work_mode; heat/cool/auto_temp_set
#     (dp 151/152/153) are the per-mode stored setpoints. All exposed as number entities.
#   - auto_temp_set (dp 153) declares scale:1 in the Tuya model while sibling setpoints
#     declare scale:0. Treated as scale:0 to match observed behavior; revisit if the
#     device returns divide-by-10 values in practice.
#   - reset (dp 198) is write-only (accessMode: "wr") — not exposed as a standard entity.
# ====================================================

SENSOR_TYPES = {
    "temp_current": {
        "dp_id": 16,
        "code": "temp_current",
        "name": "Current Temperature",
        "unit": "°C",
        "icon": "mdi:thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
    },
    "temp_current_f": {
        "dp_id": 35,
        "code": "temp_current_f",
        "name": "Current Temperature (°F)",
        "unit": "°F",
        "icon": "mdi:thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
    },
}

BINARY_SENSOR_TYPES = {
    "fault": {
        "dp_id": 15,
        "code": "fault",
        "name": "Fault Alarm",
        "device_class": "problem",
        "conversion": "value != 0"
    },
    "fan_module_fault_1": {
        "dp_id": 196,
        "code": "fan_module_fault_1",
        "name": "Fan Module 1 Fault",
        "device_class": "problem",
        "conversion": "value != 0"
    },
    "fan_module_fault_2": {
        "dp_id": 197,
        "code": "fan_module_fault_2",
        "name": "Fan Module 2 Fault",
        "device_class": "problem",
        "conversion": "value != 0"
    },
    "custom_fault_bit": {
        "dp_id": 199,
        "code": "custom_fault_bit",
        "name": "Inverter Module Fault",
        "device_class": "problem",
        "conversion": "value != 0"
    },
}

SWITCH_TYPES = {
    "switch": {
        "dp_id": 1,
        "code": "switch",
        "name": "Power",
        "icon": "mdi:power",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']"
    },
}

NUMBER_TYPES = {
    "temp_set": {
        "dp_id": 4,
        "code": "temp_set",
        "name": "Target Temperature",
        "icon": "mdi:thermometer",
        "unit": "°C",
        "min_value": 10.0,
        "max_value": 75.0,
        "step": 1.0,
        "conversion": "value",
        "api_conversion": "round(value)"
    },
    "heat_temp_set": {
        "dp_id": 151,
        "code": "heat_temp_set",
        "name": "Heat Mode Setpoint",
        "icon": "mdi:thermometer-plus",
        "unit": "°C",
        "min_value": 5.0,
        "max_value": 75.0,
        "step": 1.0,
        "conversion": "value",
        "api_conversion": "round(value)"
    },
    "cool_temp_set": {
        "dp_id": 152,
        "code": "cool_temp_set",
        "name": "Cool Mode Setpoint",
        "icon": "mdi:thermometer-minus",
        "unit": "°C",
        "min_value": 8.0,
        "max_value": 40.0,
        "step": 1.0,
        "conversion": "value",
        "api_conversion": "round(value)"
    },
    "auto_temp_set": {
        "dp_id": 153,
        "code": "auto_temp_set",
        "name": "Auto Mode Setpoint",
        "icon": "mdi:thermometer-auto",
        "unit": "°C",
        "min_value": 8.0,
        "max_value": 40.0,
        "step": 1.0,
        "conversion": "value",
        "api_conversion": "round(value)"
    },
}

SELECT_TYPES = {
    "work_mode": {
        "dp_id": 5,
        "code": "work_mode",
        "name": "Work Mode",
        "icon": "mdi:hvac",
        "options": {
            "heat": "Heat",
            "cool": "Cool",
            "auto": "Auto"
        },
    },
    "mode": {
        "dp_id": 2,
        "code": "mode",
        "name": "Frequency Mode",
        "icon": "mdi:speedometer",
        "options": {
            "smart": "Smart",
            "strong": "Strong",
            "mute": "Silent"
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
