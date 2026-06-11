"""Model mapping for Ivapool Heat Pump (000004kb7r)."""

MODEL_NAME = "Ivapool Heat Pump (000004kb7r)"
# ====================================================
# Ivapool @fehrudi87
# ====================================================

# ====================================================
# SENSOR TYPES (read-only value - accessMode: "ro")
# ====================================================
SENSOR_TYPES = {
    # Current Temperature (dp_id: 108)
    "temp_current1": {
        "dp_id": 108,
        "code": "temp_current1",
        "name": "Current Temperature",
        "unit": "°C",
        "icon": "mdi:thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
        "conversion": "(value - 32) * 5/9",
    },
    # Compressor Strength (dp_id: 109)
    "compressor_strength": {
        "dp_id": 109,
        "code": "compressor_strength",
        "name": "Compressor Strength",
        "unit": "%",
        "icon": "mdi:engine",
        "state_class": "measurement",
    },
    # Temperature Upper Limit (dp_id: 110)
    "temp_top": {
        "dp_id": 110,
        "code": "temp_top",
        "name": "Temperature Upper Limit",
        "unit": "°C",
        "icon": "mdi:thermometer-chevron-up",
        "device_class": "temperature",
        "state_class": "measurement",
        "conversion": "(value - 32) * 5/9",
    },
    # Temperature Lower Limit (dp_id: 111)
    "temp_bottom": {
        "dp_id": 111,
        "code": "temp_bottom",
        "name": "Temperature Lower Limit",
        "unit": "°C",
        "icon": "mdi:thermometer-chevron-down",
        "device_class": "temperature",
        "state_class": "measurement",
        "conversion": "(value - 32) * 5/9",
    },
    # Outdoor Coil Temperature (dp_id: 112)
    "temp_coiler": {
        "dp_id": 112,
        "code": "temp_coiler",
        "name": "Outdoor Coil Temperature",
        "unit": "°C",
        "icon": "mdi:thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
        "conversion": "(value - 32) * 5/9",
    },
    # Exhaust / Discharge Temperature (dp_id: 113)
    "temp_venting": {
        "dp_id": 113,
        "code": "temp_venting",
        "name": "Exhaust Temperature",
        "unit": "°C",
        "icon": "mdi:thermometer-alert",
        "device_class": "temperature",
        "state_class": "measurement",
        "conversion": "(value - 32) * 5/9",
    },
    # Outlet Water Temperature (dp_id: 114)
    "temp_effluent": {
        "dp_id": 114,
        "code": "temp_effluent",
        "name": "Outlet Water Temperature",
        "unit": "°C",
        "icon": "mdi:thermometer-water",
        "device_class": "temperature",
        "state_class": "measurement",
        "conversion": "(value - 32) * 5/9",
    },
    # Ambient Temperature (dp_id: 115)
    "temp_around": {
        "dp_id": 115,
        "code": "temp_around",
        "name": "Ambient Temperature",
        "unit": "°C",
        "icon": "mdi:home-thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
        "conversion": "(value - 32) * 5/9",
    },
    # Inlet Water Temperature (dp_id: 117)
    "temp_inflow": {
        "dp_id": 117,
        "code": "temp_inflow",
        "name": "Inlet Water Temperature",
        "unit": "°C",
        "icon": "mdi:thermometer-water",
        "device_class": "temperature",
        "state_class": "measurement",
        "conversion": "(value - 32) * 5/9",
    },
    # Suction / Return Gas Temperature (dp_id: 118)
    "temp_return": {
        "dp_id": 118,
        "code": "temp_return",
        "name": "Suction Temperature",
        "unit": "°C",
        "icon": "mdi:thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
        "conversion": "(value - 32) * 5/9",
    },
    # Indoor Coil Temperature (dp_id: 119)
    "temp_coiler_inside": {
        "dp_id": 119,
        "code": "temp_coiler_inside",
        "name": "Indoor Coil Temperature",
        "unit": "°C",
        "icon": "mdi:thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
        "conversion": "(value - 32) * 5/9",
    },
    # Radiator Temperature (dp_id: 120)
    "temp_radiator": {
        "dp_id": 120,
        "code": "temp_radiator",
        "name": "Radiator Temperature",
        "unit": "°C",
        "icon": "mdi:thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
        "conversion": "(value - 32) * 5/9",
    },
    # Electronic Expansion Valve Opening (dp_id: 121)
    "expansion_valve": {
        "dp_id": 121,
        "code": "expansion_valve",
        "name": "Expansion Valve Opening",
        "unit": "P",
        "icon": "mdi:pipe-valve",
        "state_class": "measurement",
    },
    # Power (dp_id: 125) - scale: 3 (value / 1000)
    "power": {
        "dp_id": 125,
        "code": "power",
        "name": "Power",
        "unit": "kW",
        "icon": "mdi:flash",
        "device_class": "power",
        "state_class": "measurement",
        "conversion": "value / 1000",
    },
    # Fault 1 - Raw Bitmap Value (dp_id: 107)
    "fault1_code": {
        "dp_id": 107,
        "code": "fault1_code",
        "name": "Fault Code 1",
        "icon": "mdi:alert-circle",
        "device_class": "problem",
        "state_class": "measurement",
    },
    # Fault 2 - Raw Bitmap Value (dp_id: 116)
    "fault2_code": {
        "dp_id": 116,
        "code": "fault2_code",
        "name": "Fault Code 2",
        "icon": "mdi:alert-circle",
        "device_class": "problem",
        "state_class": "measurement",
    },
}

# ====================================================
# BINARY SENSOR TYPES (read-only bool/bitmap - accessMode: "ro")
# ====================================================
BINARY_SENSOR_TYPES = {
    # Fault 1 Status (dp_id: 107)
    "fault1": {
        "dp_id": 107,
        "code": "fault1",
        "name": "Fault Status 1",
        "device_class": "problem",
        "conversion": "value != 0",
    },
    # Fault 2 Status (dp_id: 116)
    "fault2": {
        "dp_id": 116,
        "code": "fault2",
        "name": "Fault Status 2",
        "device_class": "problem",
        "conversion": "value != 0",
    },
    # Power Display Enable (dp_id: 122)
    "power_w": {
        "dp_id": 122,
        "code": "power_w",
        "name": "Power Display Enable",
        "icon": "mdi:eye",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']",
    },
    # Cooling Enable (dp_id: 123) - 0: Single Temp Mode, 1: Dual Temp Mode
    "cool_enable": {
        "dp_id": 123,
        "code": "cool_enable",
        "name": "Cooling Enable",
        "icon": "mdi:snowflake",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']",
    },
}

# ====================================================
# SWITCH TYPES (read-write bool - accessMode: "rw")
# ====================================================
SWITCH_TYPES = {
    # Power Switch (dp_id: 101)
    "switch1": {
        "dp_id": 101,
        "code": "switch1",
        "name": "Power",
        "icon": "mdi:power",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']",
    },
    # Child Lock (dp_id: 103)
    "child_lock1": {
        "dp_id": 103,
        "code": "child_lock1",
        "name": "Child Lock",
        "icon": "mdi:lock",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']",
    },
}

# ====================================================
# NUMBER TYPES (read-write value - accessMode: "rw")
# ====================================================
NUMBER_TYPES = {
    # Target Temperature Setpoint (dp_id: 104)
    # Cihaz dahili olarak Fahrenheit kullanıyor, dönüşüm yapıyoruz
    "temp_set1": {
        "dp_id": 104,
        "code": "temp_set1",
        "name": "Target Temperature",
        "icon": "mdi:thermostat",
        "unit": "°C",
        "min_value": -30.0,  # -22°F ≈ -30°C
        "max_value": 40.0,   # 104°F ≈ 40°C
        "step": 1.0,
        "api_conversion": "(value * 9/5) + 32",  # °C → °F
    },
}

# ====================================================
# SELECT TYPES (read-write enum - accessMode: "rw")
# ====================================================
SELECT_TYPES = {
    # Mode (dp_id: 102) - auto, heating, cold
    "mode1": {
        "dp_id": 102,
        "code": "mode1",
        "name": "Mode",
        "icon": "mdi:hvac",
        "options": {
            "auto": "Auto",
            "heating": "Heating",
            "cold": "Cooling",
        },
    },
    # Work Mode (dp_id: 105) - power, boost, silence, perfect
    "work_mode": {
        "dp_id": 105,
        "code": "work_mode",
        "name": "Work Mode",
        "icon": "mdi:cog",
        "options": {
            "power": "Power",
            "boost": "Boost",
            "silence": "Silence",
            "perfect": "Perfect",
        },
    },
    # Temperature Unit (dp_id: 106) - f, c
    "temp_unit_convert1": {
        "dp_id": 106,
        "code": "temp_unit_convert1",
        "name": "Temperature Unit",
        "icon": "mdi:thermometer",
        "options": {
            "c": "Celsius",
            "f": "Fahrenheit",
        },
    },
    # Overclock Mode (dp_id: 124) - read-only
    "oc_mode": {
        "dp_id": 124,
        "code": "oc_mode",
        "name": "Overclock Mode",
        "icon": "mdi:speedometer",
        "options": {
            "oc_0": "No Overclock",
            "oc_1": "Overclock Mode 1",
            "oc_2": "Overclock Mode 2",
        },
    },
}
