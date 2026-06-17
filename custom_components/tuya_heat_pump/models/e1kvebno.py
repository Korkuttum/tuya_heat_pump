"""Model mapping for W'eau Heat Pump (e1kvebno)."""

MODEL_NAME = "W'eau Heat Pump (e1kvebno)"
# ====================================================
# W'eau @rznq0q
# ====================================================
SENSOR_TYPES = {
    "temp_current": {
        "dp_id": 10,
        "code": "temp_current",
        "name": "Current Temperature",
        "unit": "°C",
        "icon": "mdi:thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
        "conversion": "value / 10",
    },
    "machine_type": {
        "dp_id": 101,
        "code": "machine_type",
        "name": "Machine Type",
        "icon": "mdi:information",
        "options": {
            0: "Mini (eh/ec)",
            1: "4 Mode (bh/eh/ec/auto)",
            2: "7 Mode (bh/eh/sh/bc/ec/sc/auto)",
            3: "ZK 4 Mode (eh/sh/ec/auto)"
        }
    },
    "temp_up": {
        "dp_id": 102,
        "code": "temp_up",
        "name": "Temperature Upper Limit",
        "unit": "°C",
        "icon": "mdi:thermometer-chevron-up",
        "device_class": "temperature",
        "state_class": "measurement",
    },
    "temp_low": {
        "dp_id": 103,
        "code": "temp_low",
        "name": "Temperature Lower Limit",
        "unit": "°C",
        "icon": "mdi:thermometer-chevron-down",
        "device_class": "temperature",
        "state_class": "measurement",
    },
    "fault": {
        "dp_id": 20,
        "code": "fault",
        "name": "Fault Codes",
        "icon": "mdi:alert-circle",
        "device_class": "problem",
        "options": {
            1: "E01 - Phase Error",
            2: "E02 - Phase Loss",
            4: "E03 - Water Flow Protection",
            8: "E04 - Anti-Freeze Protection",
            16: "E05 - High Pressure Protection",
            32: "E06 - Low Pressure Protection",
            64: "E09 - Communication Fault",
            128: "E10 - Inverter Communication Fault",
            256: "E12 - High Exhaust Temperature",
            512: "E15 - Inlet Water Sensor Fault",
            1024: "E16 - Coil Sensor Fault",
            2048: "E18 - Exhaust Sensor Fault",
            4096: "E20 - Inverter Module Fault",
            8192: "E21 - Ambient Sensor Fault",
            16384: "E23 - Low Outlet Temp (Cooling)",
            32768: "E27 - Outlet Water Sensor Fault",
            65536: "E29 - Suction Gas Sensor Fault",
            131072: "E32 - High Outlet Temp (Heating)",
            262144: "E33 - High Outdoor Coil Temp",
            524288: "E35 - Compressor Overcurrent",
            1048576: "E36 - DC Fan Fault",
            2097152: "E42 - Cooling Coil Sensor Fault",
            4194304: "E44 - Low Ambient Temp Protection",
            8388608: "E45 - High Ambient Temp Protection",
        }
    },
}

# ====================================================
# BINARY SENSOR TYPES (read-only bool - accessMode: "ro")
# ====================================================
BINARY_SENSOR_TYPES = {
    "temp_unit": {
        "dp_id": 104,
        "code": "temp_unit",
        "name": "Temperature Unit",
        "icon": "mdi:thermometer",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']",
        "options": {
            True: "Celsius",
            False: "Fahrenheit"
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
        "dp_id": 9,
        "code": "temp_set",
        "name": "Temperature Setpoint",
        "icon": "mdi:thermostat",
        "unit": "°C",
        "min_value": 8.0,
        "max_value": 40.0,
        "step": 1.0,
        "conversion": "int(value)",        # okuma için
        "api_conversion": "int(value)"
    },
}

# ====================================================
# SELECT TYPES (read-write enum - accessMode: "rw")
# ====================================================
SELECT_TYPES = {
    "mode": {
        "dp_id": 2,
        "code": "mode",
        "name": "Mode",
        "icon": "mdi:hvac",
        "options": {
            "bheat": "Powerful Heating",
            "eheat": "Smart Heating",
            "sheat": "Silent Heating",
            "bcool": "Powerful Cooling",
            "ecool": "Smart Cooling",
            "scool": "Silent Cooling",
            "auto": "Auto"
        },
    },
}
