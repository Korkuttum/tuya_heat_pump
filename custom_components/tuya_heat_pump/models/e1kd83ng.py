"""Model mapping for Poolsana Heat Pump (e1kd83ng)."""

MODEL_NAME = "Poolsana Heat Pump (e1kd83ng)"
# ====================================================
# Poolsana Heat Pump @rommelfs
# ====================================================
SENSOR_TYPES = {
    "temp_current": {
        "dp_id": 16,
        "code": "temp_current",
        "name": "Inlet Water Temperature",
        "unit": "°C",
        "icon": "mdi:thermometer-water",
        "device_class": "temperature",
        "state_class": "measurement",
        "conversion": "value / 10",
    },
    "effluent_temp": {
        "dp_id": 25,
        "code": "effluent_temp",
        "name": "Outlet Water Temperature",
        "unit": "°C",
        "icon": "mdi:thermometer-water",
        "device_class": "temperature",
        "state_class": "measurement",
        "conversion": "value / 10",
    },
    "return_temp": {
        "dp_id": 121,
        "code": "return_temp",
        "name": "Suction / Return Temperature",
        "unit": "°C",
        "icon": "mdi:thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
        "conversion": "value / 10",
    },
    
    # ========== HEAT PUMP COMPONENT TEMPERATURES (Celsius) ==========
    "coiler_temp": {
        "dp_id": 23,
        "code": "coiler_temp",
        "name": "Heating Coil Temperature",
        "unit": "°C",
        "icon": "mdi:thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
        "conversion": "value / 10",
    },
    "venting_temp": {
        "dp_id": 24,
        "code": "venting_temp",
        "name": "Discharge / Venting Temperature",
        "unit": "°C",
        "icon": "mdi:thermometer-alert",
        "device_class": "temperature",
        "state_class": "measurement",
        "conversion": "value / 10",
    },
    "around_temp": {
        "dp_id": 26,
        "code": "around_temp",
        "name": "Ambient / Around Temperature",
        "unit": "°C",
        "icon": "mdi:home-thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
        "conversion": "value / 10",
    },
    "cool_coiler_temp": {
        "dp_id": 123,
        "code": "cool_coiler_temp",
        "name": "Cooling Coil Temperature",
        "unit": "°C",
        "icon": "mdi:thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
        "conversion": "value / 10",
    },

    # ========== FAHRENHEIT VERSIONS (read-only) ==========
    "temp_current_f": {
        "dp_id": 35,
        "code": "temp_current_f",
        "name": "Inlet Water Temperature",
        "unit": "°F",
        "icon": "mdi:thermometer-water",
        "device_class": "temperature",
        "state_class": "measurement",
    },
    "effluent_temp_f": {
        "dp_id": 40,
        "code": "effluent_temp_f",
        "name": "Outlet Water Temperature",
        "unit": "°F",
        "icon": "mdi:thermometer-water",
        "device_class": "temperature",
        "state_class": "measurement",
    },
    "return_temp_f": {
        "dp_id": 122,
        "code": "return_temp_f",
        "name": "Suction / Return Temperature",
        "unit": "°F",
        "icon": "mdi:thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
    },
    "coiler_temp_f": {
        "dp_id": 41,
        "code": "coiler_temp_f",
        "name": "Heating Coil Temperature",
        "unit": "°F",
        "icon": "mdi:thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
    },
    "venting_temp_f": {
        "dp_id": 39,
        "code": "venting_temp_f",
        "name": "Discharge / Venting Temperature",
        "unit": "°F",
        "icon": "mdi:thermometer-alert",
        "device_class": "temperature",
        "state_class": "measurement",
    },
    "around_temp_f": {
        "dp_id": 38,
        "code": "around_temp_f",
        "name": "Ambient / Around Temperature",
        "unit": "°F",
        "icon": "mdi:home-thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
    },
    "cool_coiler_temp_f": {
        "dp_id": 124,
        "code": "cool_coiler_temp_f",
        "name": "Cooling Coil Temperature",
        "unit": "°F",
        "icon": "mdi:thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
    },

    # ========== UNIT INFORMATION ==========
    "unit_type": {
        "dp_id": 109,
        "code": "unit_type",
        "name": "Unit Type",
        "icon": "mdi:information",
        "options": {
            0: "Standard",
            1: "Inverter"
        }
    },
    
    # ========== VALVE POSITION ==========
    "opening": {
        "dp_id": 125,
        "code": "opening",
        "name": "Electronic Expansion Valve Opening",
        "unit": "P",
        "icon": "mdi:pipe-valve",
        "state_class": "measurement",
    },
    
    # ========== WORK STATE (read-only enum - accessMode: "ro") ==========
    "work_state": {
        "dp_id": 17,
        "code": "work_state",
        "name": "Work State",
        "icon": "mdi:state-machine",
        "options": {
            "Running": "Running",
            "Defrosting": "Defrosting",
            "Standby": "Standby",
            "Fault": "Fault"
        }
    },
    
    # ========== TEMPERATURE SETPOINTS (read-only for display) ==========
    "set_heating_temp": {
        "dp_id": 101,
        "code": "set_heating_temp",
        "name": "Heating Target Temperature",
        "unit": "°C",
        "icon": "mdi:thermostat",
        "device_class": "temperature",
        "state_class": "measurement",
        "conversion": "value / 10",
    },
    "set_cold_temp": {
        "dp_id": 102,
        "code": "set_cold_temp",
        "name": "Cooling Target Temperature",
        "unit": "°C",
        "icon": "mdi:snowflake",
        "device_class": "temperature",
        "state_class": "measurement",
        "conversion": "value / 10",
    },
    "set_auto_temp": {
        "dp_id": 104,
        "code": "set_auto_temp",
        "name": "Auto Target Temperature",
        "unit": "°C",
        "icon": "mdi:thermostat-auto",
        "device_class": "temperature",
        "state_class": "measurement",
        "conversion": "value / 10",
    },
    "set_heating_temp_f": {
        "dp_id": 105,
        "code": "set_heating_temp_f",
        "name": "Heating Target Temperature",
        "unit": "°F",
        "icon": "mdi:thermostat",
        "device_class": "temperature",
        "state_class": "measurement",
    },
    "set_cold_temp_f": {
        "dp_id": 106,
        "code": "set_cold_temp_f",
        "name": "Cooling Target Temperature",
        "unit": "°F",
        "icon": "mdi:snowflake",
        "device_class": "temperature",
        "state_class": "measurement",
    },
    "set_auto_temp_f": {
        "dp_id": 108,
        "code": "set_auto_temp_f",
        "name": "Auto Target Temperature",
        "unit": "°F",
        "icon": "mdi:thermostat-auto",
        "device_class": "temperature",
        "state_class": "measurement",
    },
}

# ====================================================
# BINARY SENSOR TYPES (read-only bool/bitmap - accessMode: "ro")
# ====================================================
BINARY_SENSOR_TYPES = {
    # Main Fault Status
    "fault": {
        "dp_id": 15,
        "code": "fault",
        "name": "Fault Alarm",
        "device_class": "problem",
        "conversion": "value != 0"
    },
    # Detailed Fault Code Tables
    "new_fault_01": {
        "dp_id": 103,
        "code": "new_fault_01",
        "name": "Fault Code Table 1",
        "device_class": "problem",
        "conversion": "value != 0"
    },
    "new_fault_02": {
        "dp_id": 107,
        "code": "new_fault_02",
        "name": "Fault Code Table 2",
        "device_class": "problem",
        "conversion": "value != 0"
    },
    "fault_2": {
        "dp_id": 118,
        "code": "fault_2",
        "name": "Fault Alarm 2",
        "device_class": "problem",
        "conversion": "value != 0"
    },
    "fault_3": {
        "dp_id": 119,
        "code": "fault_3",
        "name": "Fault Alarm 3",
        "device_class": "problem",
        "conversion": "value != 0"
    },
    # Driver Faults
    "new_driver_fault_01": {
        "dp_id": 110,
        "code": "new_driver_fault_01",
        "name": "Driver Fault Code Table 1",
        "device_class": "problem",
        "conversion": "value != 0"
    },
    "new_driver_fault_02": {
        "dp_id": 111,
        "code": "new_driver_fault_02",
        "name": "Driver Fault Code Table 2",
        "device_class": "problem",
        "conversion": "value != 0"
    },
    "driver_fault_1": {
        "dp_id": 120,
        "code": "driver_fault_1",
        "name": "Driver Fault",
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
}

# ====================================================
# NUMBER TYPES (read-write value - accessMode: "rw")
# ====================================================
NUMBER_TYPES = {
    "set_heating_temp": {
        "dp_id": 101,
        "code": "set_heating_temp",
        "name": "Heating Target Temperature",
        "icon": "mdi:thermostat",
        "unit": "°C",
        "min_value": 15.0,
        "max_value": 40.0,
        "step": 1.0,
        "conversion": "value / 10",
        "api_conversion": "value * 10"
    },
    "set_cold_temp": {
        "dp_id": 102,
        "code": "set_cold_temp",
        "name": "Cooling Target Temperature",
        "icon": "mdi:snowflake",
        "unit": "°C",
        "min_value": 8.0,
        "max_value": 28.0,
        "step": 1.0,
        "conversion": "value / 10",
        "api_conversion": "value * 10"
    },
    "set_auto_temp": {
        "dp_id": 104,
        "code": "set_auto_temp",
        "name": "Auto Target Temperature",
        "icon": "mdi:thermostat-auto",
        "unit": "°C",
        "min_value": 8.0,
        "max_value": 40.0,
        "step": 1.0,
        "conversion": "value / 10",
        "api_conversion": "value * 10"
    },
    "set_heating_temp_f": {
        "dp_id": 105,
        "code": "set_heating_temp_f",
        "name": "Heating Target Temperature",
        "icon": "mdi:thermostat",
        "unit": "°F",
        "min_value": 59.0,
        "max_value": 104.0,
        "step": 1.0,
        "api_conversion": "value"
    },
    "set_cold_temp_f": {
        "dp_id": 106,
        "code": "set_cold_temp_f",
        "name": "Cooling Target Temperature",
        "icon": "mdi:snowflake",
        "unit": "°F",
        "min_value": 46.0,
        "max_value": 82.0,
        "step": 1.0,
        "api_conversion": "value"
    },
    "set_auto_temp_f": {
        "dp_id": 108,
        "code": "set_auto_temp_f",
        "name": "Auto Target Temperature",
        "icon": "mdi:thermostat-auto",
        "unit": "°F",
        "min_value": 46.0,
        "max_value": 104.0,
        "step": 1.0,
        "api_conversion": "value"
    },
}

# ====================================================
# SELECT TYPES (read-write enum - accessMode: "rw")
# ====================================================
SELECT_TYPES = {
    # Operating Mode (Smart/Powerful/Silent)
    "mode": {
        "dp_id": 2,
        "code": "mode",
        "name": "Operating Mode",
        "icon": "mdi:hvac",
        "options": {
            "Auto": "Auto",
            "Heating_Powerful": "Heating (Powerful)",
            "Cooling_Powerful": "Cooling (Powerful)",
            "Heating_Smart": "Heating (Smart)",
            "Cooling_Smart": "Cooling (Smart)",
            "Heating_Silent": "Heating (Silent)",
            "Cooling_Silent": "Cooling (Silent)"
        },
    },
    # Work Mode (Cool/Heat/Auto)
    "work_mode": {
        "dp_id": 5,
        "code": "work_mode",
        "name": "Work Mode",
        "icon": "mdi:air-conditioner",
        "options": {
            "Cool_mode": "Cooling",
            "Heat_mode": "Heating",
            "Auto_mode": "Auto"
        },
    },
    # Temperature Unit
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
    # Frequency Mode (read-write enum)
    "frequency": {
        "dp_id": 117,
        "code": "frequency",
        "name": "Frequency Mode",
        "icon": "mdi:sine-wave",
        "options": {
            "Silent": "Silent",
            "Smart": "Smart",
            "Powerful": "Powerful"
        },
    },
}
