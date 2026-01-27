"""Model mapping for 000003ynwv Tuya Heat Pump."""

MODEL_NAME = "Tuya Heat Pump (000003ynwv)"
# ====================================================
# MyCond BeeThermic @RuslanNovak
# ====================================================
SENSOR_TYPES = {
    "power_consumption": {
        "dp_id": 18,
        "code": "power_consumption",
        "name": "Today's Energy",
        "unit": "kWh",
        "icon": "mdi:flash",
        "device_class": "energy",
        "state_class": "total_increasing",
        "conversion": "value / 100"
    },
    "temp_top": {
        "dp_id": 21,
        "code": "temp_top",
        "name": "Inlet Water Temperature",
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
        "icon": "mdi:thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
        "conversion": "value"
    },
    "cur_current": {
        "dp_id": 102,
        "code": "cur_current",
        "name": "Current",
        "unit": "A",
        "icon": "mdi:current-ac",
        "device_class": "current",
        "state_class": "measurement",
        "conversion": "value / 1000"
    },
    "voltage_current": {
        "dp_id": 103,
        "code": "voltage_current",
        "name": "Voltage",
        "unit": "V",
        "icon": "mdi:lightning-bolt",
        "device_class": "voltage",
        "state_class": "measurement",
        "conversion": "value / 10"
    },
    "cur_power": {
        "dp_id": 104,
        "code": "cur_power",
        "name": "Power",
        "unit": "W",
        "icon": "mdi:flash",
        "device_class": "power",
        "state_class": "measurement",
        "conversion": "value / 10"
    },
    "electric_total": {
        "dp_id": 105,
        "code": "electric_total",
        "name": "Total Energy",
        "unit": "kWh",
        "icon": "mdi:chart-line",
        "device_class": "energy",
        "state_class": "total_increasing",
        "conversion": "value / 100"
    },
}

# ====================================================
# BINARY SENSOR TYPES (read-only)
# ====================================================
BINARY_SENSOR_TYPES = {
    "fault": {
        "dp_id": 15,
        "code": "fault",
        "name": "Fault Status",
        "device_class": "problem",
        "conversion": "value != 0"
    },
    "defrost_state": {
        "dp_id": 33,
        "code": "defrost_state",
        "name": "Defrost State",
        "device_class": "cold",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']"
    },
}

# ====================================================
# SWITCH TYPES (read-write)
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
# NUMBER TYPES (read-write)
# ====================================================
NUMBER_TYPES = {
    "temp_set": {
        "dp_id": 4,
        "code": "temp_set",
        "name": "Temperature Setpoint",
        "icon": "mdi:thermometer",
        "unit": "°C",
        "min_value": 5.0,
        "max_value": 80.0,
        "step": 1.0,
        "conversion": "value",
        "api_conversion": "value"
    },
    "water_set": {
        "dp_id": 10,
        "code": "water_set",
        "name": "Control Temperature",
        "icon": "mdi:thermometer-water",
        "unit": "L",
        "min_value": 0.0,
        "max_value": 1.0,
        "step": 1.0,
        "conversion": "value",
        "api_conversion": "value"
    },
    "minitemp_set": {
        "dp_id": 101,
        "code": "minitemp_set",
        "name": "Hot Water Temperature Set",
        "icon": "mdi:water-thermometer",
        "unit": "°C",
        "min_value": 5.0,
        "max_value": 80.0,
        "step": 1.0,
        "conversion": "value",
        "api_conversion": "value"
    },
    "volume_set": {
        "dp_id": 106,
        "code": "volume_set",
        "name": "Power Detection Module",
        "icon": "mdi:meter-electric",
        "unit": "",
        "min_value": 0.0,
        "max_value": 1.0,
        "step": 1.0,
        "conversion": "value",
        "api_conversion": "value"
    },
}

# ====================================================
# SELECT TYPES (read-write)
# ====================================================
SELECT_TYPES = {
    "mode": {
        "dp_id": 2,
        "code": "mode",
        "name": "Mode",
        "icon": "mdi:air-conditioner",
        "options": {
            "cold": "Cooling",
            "heating": "Heating",
            "floor_heating": "Floor Heating",
            "hot_water": "Hot Water",
            "cold_and_hotwater": "Cool & Hot Water",
            "heating_and_hot_water": "Heat & Hot Water",
            "floor_heatign_and_hot_water": "Floor Heat & Hot Water"
        },
        "conversion": "value"
    },
    "work_mode": {
        "dp_id": 5,
        "code": "work_mode",
        "name": "Work Mode",
        "icon": "mdi:cog",
        "options": {
            "ECO": "ECO",
            "Normal": "Normal"
        },
        "conversion": "value"
    },
    "capacity_set": {
        "dp_id": 11,
        "code": "capacity_set",
        "name": "Hot Water Curve Setting",
        "icon": "mdi:chart-line",
        "options": {
            "OFF": "Off",
            "H1": "H1",
            "H2": "H2",
            "H3": "H3",
            "H4": "H4"
        },
        "conversion": "value"
    },
    "countdown_set": {
        "dp_id": 13,
        "code": "countdown_set",
        "name": "Temperature Curve Setting",
        "icon": "mdi:timer",
        "options": {
            "OFF": "Off",
            "H1": "H1",
            "H2": "H2",
            "H3": "H3",
            "H4": "H4",
            "H5": "H5",
            "H6": "H6",
            "H7": "H7",
            "H8": "H8",
            "L1": "L1",
            "L2": "L2",
            "L3": "L3",
            "L4": "L4",
            "L5": "L5",
            "L6": "L6",
            "L7": "L7",
            "L8": "L8"
        },
        "conversion": "value"
    },
}
