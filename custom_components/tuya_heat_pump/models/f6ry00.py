"""Model mapping for Heat Pump (f6ry00)."""

MODEL_NAME = "Heat Pump (f6ry00)"
# ====================================================
# Pure Blue Onyx @warrenjmcdonald
# ====================================================
SENSOR_TYPES = {
    # ========== TEMPERATURE SENSORS ==========
    "temp_current1": {
        "dp_id": 108,
        "code": "temp_current1",
        "name": "Current Temperature",
        "unit": "°C",
        "icon": "mdi:thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
    },
    "temp_top": {
        "dp_id": 110,
        "code": "temp_top",
        "name": "Temperature Upper Limit",
        "unit": "°C",
        "icon": "mdi:thermometer-chevron-up",
        "device_class": "temperature",
        "state_class": "measurement",
    },
    "temp_bottom": {
        "dp_id": 111,
        "code": "temp_bottom",
        "name": "Temperature Lower Limit",
        "unit": "°C",
        "icon": "mdi:thermometer-chevron-down",
        "device_class": "temperature",
        "state_class": "measurement",
    },
    "temp_coiler": {
        "dp_id": 112,
        "code": "temp_coiler",
        "name": "Outdoor Coil Temperature",
        "unit": "°C",
        "icon": "mdi:thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
    },
    "temp_venting": {
        "dp_id": 113,
        "code": "temp_venting",
        "name": "Discharge Temperature",
        "unit": "°C",
        "icon": "mdi:thermometer-alert",
        "device_class": "temperature",
        "state_class": "measurement",
    },
    "temp_effluent": {
        "dp_id": 114,
        "code": "temp_effluent",
        "name": "Outlet Water Temperature",
        "unit": "°C",
        "icon": "mdi:thermometer-water",
        "device_class": "temperature",
        "state_class": "measurement",
        "conversion": "value / 10",  # scale: 1
    },
    "temp_around": {
        "dp_id": 115,
        "code": "temp_around",
        "name": "Ambient Temperature",
        "unit": "°C",
        "icon": "mdi:home-thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
    },
    "temp_inflow": {
        "dp_id": 117,
        "code": "temp_inflow",
        "name": "Inlet Water Temperature",
        "unit": "°C",
        "icon": "mdi:thermometer-water",
        "device_class": "temperature",
        "state_class": "measurement",
        "conversion": "value / 10",  # scale: 1
    },
    "temp_return": {
        "dp_id": 118,
        "code": "temp_return",
        "name": "Suction Temperature",
        "unit": "°C",
        "icon": "mdi:thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
    },
    "temp_coiler_inside": {
        "dp_id": 119,
        "code": "temp_coiler_inside",
        "name": "Indoor Coil Temperature",
        "unit": "°C",
        "icon": "mdi:thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
    },
    "temp_radiator": {
        "dp_id": 120,
        "code": "temp_radiator",
        "name": "Radiator Temperature",
        "unit": "°C",
        "icon": "mdi:thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
    },
    
    # ========== COMPRESSOR & VALVE ==========
    "compressor_strength": {
        "dp_id": 109,
        "code": "compressor_strength",
        "name": "Compressor Strength",
        "unit": "%",
        "icon": "mdi:engine",
        "state_class": "measurement",
    },
    "expansion_valve": {
        "dp_id": 121,
        "code": "expansion_valve",
        "name": "Electronic Expansion Valve Opening",
        "unit": "P",
        "icon": "mdi:pipe-valve",
        "state_class": "measurement",
    },
    
    # ========== POWER & ENERGY ==========
    "power": {
        "dp_id": 125,
        "code": "power",
        "name": "Power",
        "unit": "kW",
        "icon": "mdi:flash",
        "device_class": "power",
        "state_class": "measurement",
        "conversion": "value / 1000",  # scale: 3
    },
    
    # ========== READ-ONLY SETPOINTS ==========
    "temp_set1": {
        "dp_id": 104,
        "code": "temp_set1",
        "name": "Temperature Setpoint",
        "unit": "°C",
        "icon": "mdi:thermostat",
        "device_class": "temperature",
        "state_class": "measurement",
    },
    
    # ========== STATUS SENSORS ==========
    "power_w": {
        "dp_id": 122,
        "code": "power_w",
        "name": "Power Display",
        "icon": "mdi:eye",
        "options": {
            0: "Not Display",
            1: "Display"
        }
    },
    "cool_enable": {
        "dp_id": 123,
        "code": "cool_enable",
        "name": "Cooling Mode",
        "icon": "mdi:snowflake",
        "options": {
            0: "Single Temperature Mode",
            1: "Dual Temperature Mode"
        }
    },
    "oc_mode": {
        "dp_id": 124,
        "code": "oc_mode",
        "name": "Overclock Mode",
        "icon": "mdi:speedometer",
        "options": {
            "oc_0": "No Overclock",
            "oc_1": "Overclock Mode 1",
            "oc_2": "Overclock Mode 2"
        }
    },
}

# ====================================================
# BINARY SENSOR TYPES (read-only bool/bitmap - accessMode: "ro")
# ====================================================
BINARY_SENSOR_TYPES = {
    "fault1": {
        "dp_id": 107,
        "code": "fault1",
        "name": "Fault Code 1",
        "device_class": "problem",
        "conversion": "value != 0"
    },
    "fault2": {
        "dp_id": 116,
        "code": "fault2",
        "name": "Fault Code 2",
        "device_class": "problem",
        "conversion": "value != 0"
    },
}

# ====================================================
# SWITCH TYPES (read-write bool - accessMode: "rw")
# ====================================================
SWITCH_TYPES = {
    "switch1": {
        "dp_id": 101,
        "code": "switch1",
        "name": "Power",
        "icon": "mdi:power",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']"
    },
    "child_lock1": {
        "dp_id": 103,
        "code": "child_lock1",
        "name": "Child Lock",
        "icon": "mdi:lock",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']"
    },
}

# ====================================================
# NUMBER TYPES (read-write value - accessMode: "rw")
# ====================================================
NUMBER_TYPES = {
    "temp_set1": {
        "dp_id": 104,
        "code": "temp_set1",
        "name": "Temperature Setpoint",
        "icon": "mdi:thermostat",
        "unit": "°C",
        "min_value": -22.0,
        "max_value": 104.0,
        "step": 1.0,
        "api_conversion": "value"
    },
}

# ====================================================
# SELECT TYPES (read-write enum - accessMode: "rw")
# ====================================================
SELECT_TYPES = {
    "mode1": {
        "dp_id": 102,
        "code": "mode1",
        "name": "Mode",
        "icon": "mdi:hvac",
        "options": {
            "auto": "Auto",
            "heating": "Heating",
            "cold": "Cooling"
        },
    },
    "work_mode": {
        "dp_id": 105,
        "code": "work_mode",
        "name": "Work Mode",
        "icon": "mdi:cog",
        "options": {
            "power": "Power",
            "boost": "Boost",
            "silence": "Silence",
            "perfect": "Perfect"
        },
    },
    "temp_unit_convert1": {
        "dp_id": 106,
        "code": "temp_unit_convert1",
        "name": "Temperature Unit",
        "icon": "mdi:thermometer",
        "options": {
            "c": "Celsius",
            "f": "Fahrenheit"
        },
    },
}
