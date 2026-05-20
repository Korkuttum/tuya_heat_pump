"""Model mapping for Weau WFI 007 Pool Heat Pump (000003p0fy)."""

MODEL_NAME = "Weau WFI 007 Pool Heat Pump"
# ====================================================
# W'eau WFI-007 @OdynBrouwer
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
        "conversion": "value / 10",  # Scale is 1, so 354 = 35.4°C
    },
}

# ====================================================
# BINARY SENSOR TYPES (read-only bool - accessMode: "ro")
# ====================================================
BINARY_SENSOR_TYPES = {
    "fault": {
        "dp_id": 6,
        "code": "fault",
        "name": "Fault Status",
        "icon": "mdi:alert-circle",
        "device_class": "problem",
        "options": {
            1: "Sensor Fault",
            2: "Exhaust Temperature Too High",
            4: "High Pressure Fault",
            8: "Low Pressure Fault",
            16: "Water Flow Fault",
            32: "Outlet Water Temperature Too High",
            64: "Outlet Water Temperature Too Low",
            128: "Water In/Out Temperature Difference Too Large",
            256: "DC Fan Fault",
            512: "Coil Temperature Too High",
            1024: "Driver Communication Fault",
            2048: "Reserved",
            4096: "Compressor Driver Fault",
            8192: "Compressor Overcurrent",
            16384: "Output Phase Loss",
            32768: "Sampling Fault",
            65536: "Emergency Stop",
            131072: "DC Voltage Too High",
            262144: "DC Voltage Too Low",
            524288: "AC Undervoltage",
            1048576: "AC Overcurrent",
            2097152: "E2 Fault",
            4194304: "AC Overvoltage",
        }
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
        "min_value": 7.0,
        "max_value": 60.0,
        "step": 1.0,
        "conversion": "value",          # Display: raw value (38 = 38°C)
        "api_conversion": "int(value)"  # Send: ensure integer type
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
            "hot": "Powerful Heating",
            "cold": "Cooling",
            "auto": "Auto",
            "eco": "Eco Heating",
        },
    },
}
