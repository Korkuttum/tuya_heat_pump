"""Model mapping for elrnos Tuya Heat Pump."""

MODEL_NAME = "Tuya Heat Pump (elrnos)"
# ====================================================
# Aquatech X6 @dabanhfreak
# ====================================================
SENSOR_TYPES = {
    # Temperature Sensors - Celsius
    "temp_current": {
        "dp_id": 16,
        "code": "temp_current",
        "name": "Tank Temperature",
        "unit": "°C",
        "icon": "mdi:water-thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
        "conversion": "value"
    },
    "compressor_strength": {
        "dp_id": 20,
        "code": "compressor_strength",
        "name": "Suction Temperature",
        "unit": "°C",
        "icon": "mdi:thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
        "conversion": "value"
    },
    "temp_top": {
        "dp_id": 21,
        "code": "temp_top",
        "name": "Coil Temperature",
        "unit": "°C",
        "icon": "mdi:thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
        "conversion": "value"
    },
    "temp_bottom": {
        "dp_id": 22,
        "code": "temp_bottom",
        "name": "Outlet Water Temperature",
        "unit": "°C",
        "icon": "mdi:thermometer-water",
        "device_class": "temperature",
        "state_class": "measurement",
        "conversion": "value"
    },
    "coiler_temp": {
        "dp_id": 23,
        "code": "coiler_temp",
        "name": "Coil Temperature",
        "unit": "°C",
        "icon": "mdi:thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
        "conversion": "value"
    },
    "venting_temp": {
        "dp_id": 24,
        "code": "venting_temp",
        "name": "Discharge Temperature",
        "unit": "°C",
        "icon": "mdi:thermometer-alert",
        "device_class": "temperature",
        "state_class": "measurement",
        "conversion": "value"
    },
    "effluent_temp": {
        "dp_id": 25,
        "code": "effluent_temp",
        "name": "Suction Temperature",
        "unit": "°C",
        "icon": "mdi:thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
        "conversion": "value"
    },
    "around_temp": {
        "dp_id": 26,
        "code": "around_temp",
        "name": "Ambient Temperature",
        "unit": "°C",
        "icon": "mdi:home-thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
        "conversion": "value"
    },
    
    # Temperature Sensors - Fahrenheit
    "temp_current_f": {
        "dp_id": 35,
        "code": "temp_current_f",
        "name": "Tank Temperature",
        "unit": "°F",
        "icon": "mdi:water-thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
        "conversion": "value"
    },
    "bottom_temp_f": {
        "dp_id": 37,
        "code": "bottom_temp_f",
        "name": "Outlet Water Temperature",
        "unit": "°F",
        "icon": "mdi:thermometer-water",
        "device_class": "temperature",
        "state_class": "measurement",
        "conversion": "value"
    },
    "around_temp_f": {
        "dp_id": 38,
        "code": "around_temp_f",
        "name": "Ambient Temperature",
        "unit": "°F",
        "icon": "mdi:home-thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
        "conversion": "value"
    },
    "venting_temp_f": {
        "dp_id": 39,
        "code": "venting_temp_f",
        "name": "Discharge Temperature",
        "unit": "°F",
        "icon": "mdi:thermometer-alert",
        "device_class": "temperature",
        "state_class": "measurement",
        "conversion": "value"
    },
    
    # Device Info & Counters
    "countdown_left": {
        "dp_id": 14,
        "code": "countdown_left",
        "name": "Electronic Expansion Valve",
        "unit": "P",
        "icon": "mdi:pipe-valve",
        "state_class": "measurement",
        "conversion": "value"
    },
    "effluent_temp_f": {
        "dp_id": 40,
        "code": "effluent_temp_f",
        "name": "Unit Assembly Number",
        "unit": "",
        "icon": "mdi:counter",
        "state_class": "measurement",
        "conversion": "value"
    },
    "coiler_temp_f": {
        "dp_id": 41,
        "code": "coiler_temp_f",
        "name": "Pre-Defrost Compressor Runtime",
        "unit": "min",
        "icon": "mdi:timer",
        "state_class": "measurement",
        "conversion": "value"
    },
    
    # Electrical Sensors (with scale conversion)
    "cur_current": {
        "dp_id": 101,
        "code": "cur_current",
        "name": "Current",
        "unit": "A",
        "icon": "mdi:current-ac",
        "device_class": "current",
        "state_class": "measurement",
        "conversion": "value / 1000"  # scale: 3
    },
    "cur_voltage": {
        "dp_id": 102,
        "code": "cur_voltage",
        "name": "Voltage",
        "unit": "V",
        "icon": "mdi:lightning-bolt",
        "device_class": "voltage",
        "state_class": "measurement",
        "conversion": "value / 10"  # scale: 1
    },
    "cur_power": {
        "dp_id": 103,
        "code": "cur_power",
        "name": "Power",
        "unit": "W",
        "icon": "mdi:flash",
        "device_class": "power",
        "state_class": "measurement",
        "conversion": "value / 10"  # scale: 1
    },
    "electric_total": {
        "dp_id": 104,
        "code": "electric_total",
        "name": "Total Energy",
        "unit": "kWh",
        "icon": "mdi:chart-line",
        "device_class": "energy",
        "state_class": "total_increasing",
        "conversion": "value / 100"  # scale: 2
    },
    
    # Power Consumption (Today's Energy)
    "power_consumption": {
        "dp_id": 18,
        "code": "power_consumption",
        "name": "Today's Energy",
        "unit": "kWh",
        "icon": "mdi:flash",
        "device_class": "energy",
        "state_class": "total_increasing",
        "conversion": "value / 100"  # scale: 2
    },
}

# ====================================================
# BINARY SENSOR TYPES (read-only bool/bitmap)
# 18 adet binary sensor entity
# ====================================================
BINARY_SENSOR_TYPES = {
    # Fault Status (bitmap)
    "fault": {
        "dp_id": 15,
        "code": "fault",
        "name": "Fault Alarm",
        "device_class": "problem",
        "conversion": "value != 0"
    },
    
    # Operation States
    "compressor_state": {
        "dp_id": 27,
        "code": "compressor_state",
        "name": "Compressor State",
        "device_class": "running",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']"
    },
    "four_valve_state": {
        "dp_id": 28,
        "code": "four_valve_state",
        "name": "4-Way Valve State",
        "device_class": "opening",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']"
    },
    "draught_fan_state": {
        "dp_id": 29,
        "code": "draught_fan_state",
        "name": "Low Pressure Switch",
        "device_class": "safety",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']"
    },
    "pump_state": {
        "dp_id": 30,
        "code": "pump_state",
        "name": "Refrigerant/Water Cycle",
        "icon": "mdi:water-pump",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']"
    },
    "backwater": {
        "dp_id": 31,
        "code": "backwater",
        "name": "Pump State",
        "device_class": "running",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']"
    },
    "ele_heating_state": {
        "dp_id": 32,
        "code": "ele_heating_state",
        "name": "Electric Heating State",
        "device_class": "heat",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']"
    },
    "defrost_state": {
        "dp_id": 33,
        "code": "defrost_state",
        "name": "High Pressure Switch",
        "device_class": "safety",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']"
    },
    "defrost": {
        "dp_id": 7,
        "code": "defrost",
        "name": "Defrosting",
        "device_class": "cold",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']"
    },
    
    # Electrical & Protection
    "lpress": {
        "dp_id": 105,
        "code": "lpress",
        "name": "Power Detection",
        "device_class": "power",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']"
    },
    "link": {
        "dp_id": 106,
        "code": "link",
        "name": "Linkage Switch",
        "device_class": "connectivity",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']"
    },
    "flowswitch": {
        "dp_id": 107,
        "code": "flowswitch",
        "name": "Water Flow Switch",
        "device_class": "running",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']"
    },
    
    # DIP Switches
    "sw1": {
        "dp_id": 108,
        "code": "sw1",
        "name": "DIP Switch 1",
        "icon": "mdi:dip-switch",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']"
    },
    "sw2": {
        "dp_id": 109,
        "code": "sw2",
        "name": "DIP Switch 2",
        "icon": "mdi:dip-switch",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']"
    },
    
    # Cooling Available
    "cancool": {
        "dp_id": 110,
        "code": "cancool",
        "name": "Cooling Available",
        "device_class": "power",
        "icon": "mdi:snowflake",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']"
    },
}

# ====================================================
# SWITCH TYPES (read-write bool)
# 1 adet switch entity
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
# NUMBER TYPES (read-write value)
# 4 adet number entity
# ====================================================
NUMBER_TYPES = {
    "temp_set": {
        "dp_id": 4,
        "code": "temp_set",
        "name": "Temperature Setpoint",
        "icon": "mdi:thermostat",
        "unit": "°C",
        "min_value": 15.0,
        "max_value": 75.0,
        "step": 1.0,
        "conversion": "value",
        "api_conversion": "value"
    },
    "temp_set_f": {
        "dp_id": 34,
        "code": "temp_set_f",
        "name": "Temperature Setpoint",
        "icon": "mdi:thermostat",
        "unit": "°F",
        "min_value": 59.0,
        "max_value": 167.0,
        "step": 1.0,
        "conversion": "value",
        "api_conversion": "value"
    },
}

# ====================================================
# SELECT TYPES (read-write enum)
# 4 adet select entity
# ====================================================
SELECT_TYPES = {
    "mode": {
        "dp_id": 2,
        "code": "mode",
        "name": "Operation Mode",
        "icon": "mdi:hvac",
        "options": {
            "Stand": "Standby",
            "ECO": "ECO Mode",
            "HYB": "Hybrid Mode",
            "HYB1": "Hybrid Mode 1",
            "ELE": "Electric Mode"
        },
        "conversion": "value"
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
        "conversion": "value"
    },
    "work_state": {
        "dp_id": 17,
        "code": "work_state",
        "name": "Phase Sequence Module",
        "icon": "mdi:flash",
        "options": {
            "normal": "Normal",
            "ERR": "Error",
            "NO": "No Status"
        },
        "conversion": "value"
    },
    "flow": {
        "dp_id": 19,
        "code": "flow",
        "name": "Fan State",
        "icon": "mdi:fan",
        "options": {
            "OFF": "Off",
            "LOW": "Low Speed",
            "High": "High Speed"
        },
        "conversion": "value"
    },
}
# ====================================================
