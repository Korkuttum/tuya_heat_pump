"""Model mapping for Cordivari Vestalis Tuya Heat Pump."""

MODEL_NAME = "Cordivari Vestalis (eu20ns)"
# ====================================================
# Cordivari Vestalis @carpenv
# Based on actual device data from 2026-02-11
# ====================================================

# ====================================================
# SENSOR TYPES (read-only value)
# ====================================================
SENSOR_TYPES = {
    # Temperature Sensors
    "temp_top": {
        "dp_id": 21,
        "code": "temp_top",
        "name": "Inlet Water Temperature",
        "unit": "°C",
        "icon": "mdi:thermometer-water",
        "device_class": "temperature",
        "state_class": "measurement",
        "conversion": "value / 10"
    },
    "temp_bottom": {
        "dp_id": 22,
        "code": "temp_bottom",
        "name": "Outlet Water Temperature",
        "unit": "°C",
        "icon": "mdi:thermometer-water",
        "device_class": "temperature",
        "state_class": "measurement",
        "conversion": "value / 10"
    },
    "coiler_temp": {
        "dp_id": 23,
        "code": "coiler_temp",
        "name": "Inlet Water Temperature",
        "unit": "°C",
        "icon": "mdi:thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
        "conversion": "value / 10"
    },
    "venting_temp": {
        "dp_id": 24,
        "code": "venting_temp",
        "name": "Outlet Water Temperature",
        "unit": "°C",
        "icon": "mdi:thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
        "conversion": "value / 10"
    },
    "effluent_temp": {
        "dp_id": 25,
        "code": "effluent_temp",
        "name": "Tank Temperature",
        "unit": "°C",
        "icon": "mdi:water-thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
        "conversion": "value / 10"
    },
    "t_liquid": {
        "dp_id": 128,
        "code": "t_liquid",
        "name": "Refrigerant Liquid Temperature",
        "unit": "°C",
        "icon": "mdi:thermometer-low",
        "device_class": "temperature",
        "state_class": "measurement",
        "conversion": "value / 10"
    },
    "t_eva": {
        "dp_id": 140,
        "code": "t_eva",
        "name": "Evaporator Temperature",
        "unit": "°C",
        "icon": "mdi:thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
        "conversion": "value / 10"
    },
    "t_con": {
        "dp_id": 141,
        "code": "t_con",
        "name": "Condenser Temperature",
        "unit": "°C",
        "icon": "mdi:thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
        "conversion": "value / 10"
    },
    "t_room1": {
        "dp_id": 139,
        "code": "t_room1",
        "name": "Room 1 Temperature",
        "unit": "°C",
        "icon": "mdi:home-thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
        "conversion": "value / 10"
    },
    "t_room2": {
        "dp_id": 145,
        "code": "t_room2",
        "name": "Room 2 Temperature",
        "unit": "°C",
        "icon": "mdi:home-thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
        "conversion": "value / 10"
    },
    "t_ipm": {
        "dp_id": 138,
        "code": "t_ipm",
        "name": "IPM Temperature",
        "unit": "°C",
        "icon": "mdi:chip",
        "device_class": "temperature",
        "state_class": "measurement",
        "conversion": "value"
    },
    
    # Compressor & Performance
    "temp_current": {
        "dp_id": 16,
        "code": "temp_current",
        "name": "Compressor Frequency",
        "unit": "Hz",
        "icon": "mdi:sine-wave",
        "device_class": "frequency",
        "state_class": "measurement",
        "conversion": "value"
    },
    "compressor_strength": {
        "dp_id": 20,
        "code": "compressor_strength",
        "name": "Discharge Temperature",
        "unit": "°C",
        "icon": "mdi:thermometer-alert",
        "device_class": "temperature",
        "state_class": "measurement",
        "conversion": "value / 10"
    },
    "i_compressor": {
        "dp_id": 137,
        "code": "i_compressor",
        "name": "Compressor Current",
        "unit": "A",
        "icon": "mdi:current-ac",
        "device_class": "current",
        "state_class": "measurement",
        "conversion": "value / 10"
    },
    "ic_drive_board": {
        "dp_id": 142,
        "code": "ic_drive_board",
        "name": "Drive Board Current",
        "unit": "A",
        "icon": "mdi:current-ac",
        "device_class": "current",
        "state_class": "measurement",
        "conversion": "value / 10"
    },
    "times_comp": {
        "dp_id": 143,
        "code": "times_comp",
        "name": "Compressor Starts",
        "unit": "times",
        "icon": "mdi:counter",
        "state_class": "total_increasing",
        "conversion": "value"
    },
    "times_defrosting": {
        "dp_id": 144,
        "code": "times_defrosting",
        "name": "Defrost Cycles",
        "unit": "times",
        "icon": "mdi:snowflake",
        "state_class": "total_increasing",
        "conversion": "value"
    },
    
    # Fans & Valves
    "fan1_rpm": {
        "dp_id": 132,
        "code": "fan1_rpm",
        "name": "Fan Speed",
        "unit": "RPM",
        "icon": "mdi:fan",
        "state_class": "measurement",
        "conversion": "value"
    },
    "valve_step_1": {
        "dp_id": 134,
        "code": "valve_step_1",
        "name": "Main Valve Opening",
        "unit": "steps",
        "icon": "mdi:pipe-valve",
        "state_class": "measurement",
        "conversion": "value"
    },
    
    # Water Flow
    "q_water": {
        "dp_id": 129,
        "code": "q_water",
        "name": "Water Flow Rate",
        "unit": "L/min",
        "icon": "mdi:water-pump",
        "state_class": "measurement",
        "conversion": "value / 10"
    },
    
    # Energy
    "power_consumption": {
        "dp_id": 18,
        "code": "power_consumption",
        "name": "Coil Temperature",
        "unit": "°C",
        "icon": "mdi:thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
        "conversion": "value / 10"
    },
    
    # Error codes (as sensors)
    "temp_current_f": {
        "dp_id": 35,
        "code": "temp_current_f",
        "name": "Error Code 07",
        "unit": "",
        "icon": "mdi:alert-circle",
        "device_class": "enum",
        "conversion": "value",
        "options": {
            "0": "No Fault",
            "1": "Acceleration Overcurrent",
            "2": "Deceleration Overcurrent",
            "3": "Constant Speed Overcurrent",
            "4": "Acceleration Overvoltage",
            "5": "Deceleration Overvoltage",
            "6": "Constant Speed Overvoltage",
            "8": "Step Out Fault",
            "9": "Phase Loss Fault",
            "10": "IPM Protection",
            "19": "Current Detection Circuit"
        }
    },
    
    # Temperature settings (read-only values)
    "p02_heating": {
        "dp_id": 117,
        "code": "p02_heating",
        "name": "Heating Set Temperature",
        "unit": "°C",
        "icon": "mdi:thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
        "conversion": "value"
    },
    "p03_cooling": {
        "dp_id": 118,
        "code": "p03_cooling",
        "name": "Cooling Set Temperature",
        "unit": "°C",
        "icon": "mdi:snowflake",
        "device_class": "temperature",
        "state_class": "measurement",
        "conversion": "value"
    },
    "p04_dhw": {
        "dp_id": 119,
        "code": "p04_dhw",
        "name": "Hot Water Set Temperature",
        "unit": "°C",
        "icon": "mdi:water-thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
        "conversion": "value"
    },
    "temp_": {
        "dp_id": 125,
        "code": "temp_",
        "name": "Master Temperature Setting",
        "unit": "°C",
        "icon": "mdi:thermostat",
        "device_class": "temperature",
        "state_class": "measurement",
        "conversion": "value"
    },
    "t_room1_setting": {
        "dp_id": 130,
        "code": "t_room1_setting",
        "name": "Room 1 Target Temperature",
        "unit": "°C",
        "icon": "mdi:thermostat-box",
        "device_class": "temperature",
        "state_class": "measurement",
        "conversion": "value"
    },
    "t_room2_setting": {
        "dp_id": 131,
        "code": "t_room2_setting",
        "name": "Room 2 Target Temperature",
        "unit": "°C",
        "icon": "mdi:thermostat-box",
        "device_class": "temperature",
        "state_class": "measurement",
        "conversion": "value / 10"
    },
}

# ====================================================
# BINARY SENSOR TYPES (read-only)
# ====================================================
BINARY_SENSOR_TYPES = {
    "fault": {
        "dp_id": 15,
        "code": "fault",
        "name": "Fault Status (Group 1)",
        "device_class": "problem",
        "conversion": "value != 0"
    },
    "smart_system": {
        "dp_id": 109,
        "code": "smart_system",
        "name": "Fault Status (Group 2)",
        "device_class": "problem",
        "conversion": "value != 0"
    },
    "power_system": {
        "dp_id": 120,
        "code": "power_system",
        "name": "Fault Status (Group 3)",
        "device_class": "problem",
        "conversion": "value != 0"
    },
    "ithium_battery_system": {
        "dp_id": 121,
        "code": "ithium_battery_system",
        "name": "Fault Status (Group 4)",
        "device_class": "problem",
        "conversion": "value != 0"
    },
    "electronic_system": {
        "dp_id": 122,
        "code": "electronic_system",
        "name": "Fault Status (Group 5)",
        "device_class": "problem",
        "conversion": "value != 0"
    },
    "bcu_com_state": {
        "dp_id": 123,
        "code": "bcu_com_state",
        "name": "Fault Status (Group 6)",
        "device_class": "problem",
        "conversion": "value != 0"
    },
    "state_way": {
        "dp_id": 135,
        "code": "state_way",
        "name": "4-Way Valve State",
        "device_class": "opening",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']"
    },
    "cooling_heating": {
        "dp_id": 124,
        "code": "cooling_heating",
        "name": "AC Temperature Setting Mode",
        "device_class": "heat",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']"
    },
}

# ====================================================
# SWITCH TYPES (read-write bool)
# ====================================================
SWITCH_TYPES = {
    "switch": {
        "dp_id": 1,
        "code": "switch",
        "name": "Power",
        "icon": "mdi:power",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']"
    },
    "child_lock": {
        "dp_id": 3,
        "code": "child_lock",
        "name": "Night Mode",
        "icon": "mdi:weather-night",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']"
    },
}

# ====================================================
# NUMBER TYPES (read-write value)
# ====================================================
NUMBER_TYPES = {
    "temp_set": {
        "dp_id": 4,
        "code": "temp_set",
        "name": "Night Mode Start Time",
        "icon": "mdi:clock-start",
        "unit": "H",
        "min_value": 0.0,
        "max_value": 23.0,
        "step": 1.0,
        "conversion": "value",
        "api_conversion": "value"
    },
    "water_set": {
        "dp_id": 10,
        "code": "water_set",
        "name": "Night Mode End Time",
        "icon": "mdi:clock-end",
        "unit": "H",
        "min_value": 0.0,
        "max_value": 23.0,
        "step": 1.0,
        "conversion": "value",
        "api_conversion": "value"
    },
    "p02_heating": {
        "dp_id": 117,
        "code": "p02_heating",
        "name": "Heating Temperature Set",
        "icon": "mdi:thermometer",
        "unit": "°C",
        "min_value": 10.0,
        "max_value": 75.0,
        "step": 1.0,
        "conversion": "value",
        "api_conversion": "value"
    },
    "p03_cooling": {
        "dp_id": 118,
        "code": "p03_cooling",
        "name": "Cooling Temperature Set",
        "icon": "mdi:snowflake",
        "unit": "°C",
        "min_value": 7.0,
        "max_value": 25.0,
        "step": 1.0,
        "conversion": "value",
        "api_conversion": "value"
    },
    "p04_dhw": {
        "dp_id": 119,
        "code": "p04_dhw",
        "name": "Hot Water Temperature Set",
        "icon": "mdi:water-thermometer",
        "unit": "°C",
        "min_value": 10.0,
        "max_value": 70.0,
        "step": 1.0,
        "conversion": "value",
        "api_conversion": "value"
    },
    "temp_": {
        "dp_id": 125,
        "code": "temp_",
        "name": "Master Temperature Set",
        "icon": "mdi:thermostat",
        "unit": "°C",
        "min_value": 7.0,
        "max_value": 75.0,
        "step": 1.0,
        "conversion": "value",
        "api_conversion": "value"
    },
    "t_room1_setting": {
        "dp_id": 130,
        "code": "t_room1_setting",
        "name": "Room 1 Temperature Set",
        "icon": "mdi:thermostat-box",
        "unit": "°C",
        "min_value": 18.0,
        "max_value": 35.0,
        "step": 1.0,
        "conversion": "value",
        "api_conversion": "value"
    },
    "t_room2_setting": {
        "dp_id": 131,
        "code": "t_room2_setting",
        "name": "Room 2 Temperature Set",
        "icon": "mdi:thermostat-box",
        "unit": "°C",
        "min_value": 18.0,
        "max_value": 35.0,
        "step": 1.0,
        "conversion": "value / 10",
        "api_conversion": "value * 10"
    },
}

# ====================================================
# SELECT TYPES (read-write enum)
# ====================================================
SELECT_TYPES = {
    "mode": {
        "dp_id": 2,
        "code": "mode",
        "name": "Operation Mode",
        "icon": "mdi:hvac",
        "options": {
            "Hot": "Hot Water Only",
            "Heating": "Heating Only",
            "Hot_Heating": "Hot Water + Heating",
            "Cooling": "Cooling Only",
            "Hot_Cooling": "Hot Water + Cooling"
        },
        "conversion": "value"
    },
}

# ====================================================
# TIME SCHEDULE INTERFACES (for future implementation)
# Note: Raw DP IDs 110-116 contain weekly schedules
# time1 (111): Monday
# time2 (112): Tuesday
# time3 (113): Wednesday
# time4 (114): Thursday
# time5 (115): Friday
# time6 (116): Saturday
# time7 (110): Sunday
# ====================================================
