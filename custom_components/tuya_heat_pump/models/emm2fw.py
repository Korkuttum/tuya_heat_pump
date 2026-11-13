# ====================================================
# Rakentaa RA040-PW13-A3 @cpiekacz, issue #116
# Tuya modelId: emm2fw
# Inverter air-to-water heat pump with enhanced vapour injection
# (EVI), hot water tank and heating / cooling.
#
# Every plain DP of the cloud schema is mapped. The first five
# values of parameter_group_1 (dp 118, 4-byte numbers) are the
# unit's main settings. Their layout comes from the tuya-local
# configuration shared by @cpiekacz, who has it working on the
# same unit. NOT mapped:
#   - the rest of parameter_group_1 and parameter_group_2 ... 7
#     (dp 119-124): raw blocks with further settings (disinfection,
#     compensation, pump and defrost parameters, ...).
#   - fault (dp 15) is a bitmap: it only tells "any fault yes/no",
#     the individual fault bits are not decoded yet.
# ====================================================
"""Model mapping for Rakentaa RA040-PW13-A3 (emm2fw)."""

MODEL_NAME = "Rakentaa RA040-PW13-A3 (emm2fw)"

# Sensor Types - all read-only, scale 0 (values are whole units)
SENSOR_TYPES = {
    "intemp": {
        "dp_id": 101,
        "code": "intemp",
        "name": "Inlet Water Temperature",
        "unit": "°C",
        "icon": "mdi:thermometer-water",
        "device_class": "temperature",
        "state_class": "measurement",
    },
    "outtemp": {
        "dp_id": 102,
        "code": "outtemp",
        "name": "Outlet Water Temperature",
        "unit": "°C",
        "icon": "mdi:thermometer-water",
        "device_class": "temperature",
        "state_class": "measurement",
    },
    "whjtemp": {
        "dp_id": 103,
        "code": "whjtemp",
        "name": "Ambient Temperature",
        "unit": "°C",
        "icon": "mdi:home-thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
    },
    "cmptemp": {
        "dp_id": 104,
        "code": "cmptemp",
        "name": "Exhaust Temperature",
        "unit": "°C",
        "icon": "mdi:thermometer-alert",
        "device_class": "temperature",
        "state_class": "measurement",
    },
    "hqtemp": {
        "dp_id": 105,
        "code": "hqtemp",
        "name": "Suction Temperature",
        "unit": "°C",
        "icon": "mdi:thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
    },
    "ptemp": {
        "dp_id": 106,
        "code": "ptemp",
        "name": "Outdoor Coil Temperature",
        "unit": "°C",
        "icon": "mdi:thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
    },
    "cptemp": {
        "dp_id": 107,
        "code": "cptemp",
        "name": "Cooling Coil Temperature",
        "unit": "°C",
        "icon": "mdi:thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
    },
    "wttemp": {
        "dp_id": 108,
        "code": "wttemp",
        "name": "Water Tank Temperature",
        "unit": "°C",
        "icon": "mdi:water-thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
    },
    "step_run": {
        "dp_id": 109,
        "code": "step_run",
        "name": "Main Expansion Valve Opening",
        "unit": "P",
        "icon": "mdi:pipe-valve",
        "state_class": "measurement",
    },
    "stepb_run": {
        "dp_id": 111,
        "code": "stepb_run",
        "name": "Enthalpy Expansion Valve Opening",
        "unit": "P",
        "icon": "mdi:pipe-valve",
        "state_class": "measurement",
    },
    "cmp_cur": {
        "dp_id": 112,
        "code": "cmp_cur",
        "name": "Compressor Current",
        "unit": "A",
        "icon": "mdi:current-ac",
        "device_class": "current",
        "state_class": "measurement",
    },
    "sink_temp": {
        "dp_id": 113,
        "code": "sink_temp",
        "name": "Heatsink Temperature",
        "unit": "°C",
        "icon": "mdi:thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
    },
    "dc_bus_voltage": {
        "dp_id": 114,
        "code": "dc_bus_voltage",
        "name": "DC Bus Voltage",
        "unit": "V",
        "icon": "mdi:lightning-bolt",
        "device_class": "voltage",
        "state_class": "measurement",
    },
    "cmp_act_frep": {
        "dp_id": 115,
        "code": "cmp_act_frep",
        "name": "Compressor Frequency",
        "unit": "Hz",
        "icon": "mdi:sine-wave",
        "device_class": "frequency",
        "state_class": "measurement",
    },
    "dc_fan_speed": {
        "dp_id": 116,
        "code": "dc_fan_speed",
        "name": "DC Fan 1 Speed",
        "unit": "RPM",
        "icon": "mdi:fan",
        "state_class": "measurement",
    },
    "dc_fan2_speed": {
        "dp_id": 117,
        "code": "dc_fan2_speed",
        "name": "DC Fan 2 Speed",
        "unit": "RPM",
        "icon": "mdi:fan",
        "state_class": "measurement",
    },
}

# Binary Sensor Types
BINARY_SENSOR_TYPES = {
    "fault": {
        # Bitmap, 0 = no fault. Individual bits are not decoded yet.
        "dp_id": 15,
        "code": "fault",
        "name": "Fault Status",
        "device_class": "problem",
        "conversion": "value != 0",
    },
}

# Switch Types - read-write booleans
SWITCH_TYPES = {
    "switch": {
        "dp_id": 1,
        "code": "switch",
        "name": "Power",
        "icon": "mdi:power",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']",
    },
}

# Number Types - read-write, 4-byte values inside the raw block parameter_group_1
NUMBER_TYPES = {
    "return_diff_heat_cool": {
        "dp_id": 118,
        "code": "return_diff_heat_cool",
        "raw_source": "parameter_group_1",
        "field_index": 0,
        "encoding": "int32_be",
        "name": "Return Difference Heating / Cooling",
        "icon": "mdi:thermometer-lines",
        "unit": "°C",
        "min_value": 2.0,
        "max_value": 18.0,
        "step": 1.0,
    },
    "return_diff_hot_water": {
        "dp_id": 118,
        "code": "return_diff_hot_water",
        "raw_source": "parameter_group_1",
        "field_index": 1,
        "encoding": "int32_be",
        "name": "Return Difference Hot Water",
        "icon": "mdi:thermometer-lines",
        "unit": "°C",
        "min_value": 2.0,
        "max_value": 18.0,
        "step": 1.0,
    },
    "hot_water_target_temp": {
        "dp_id": 118,
        "code": "hot_water_target_temp",
        "raw_source": "parameter_group_1",
        "field_index": 2,
        "encoding": "int32_be",
        "name": "Hot Water Target Temperature",
        "icon": "mdi:water-thermometer",
        "unit": "°C",
        "min_value": 28.0,
        "max_value": 55.0,
        "step": 1.0,
    },
    "cooling_target_temp": {
        "dp_id": 118,
        "code": "cooling_target_temp",
        "raw_source": "parameter_group_1",
        "field_index": 3,
        "encoding": "int32_be",
        "name": "Cooling Target Temperature",
        "icon": "mdi:snowflake-thermometer",
        "unit": "°C",
        "min_value": 12.0,
        "max_value": 30.0,
        "step": 1.0,
    },
    "heating_target_temp": {
        "dp_id": 118,
        "code": "heating_target_temp",
        "raw_source": "parameter_group_1",
        "field_index": 4,
        "encoding": "int32_be",
        "name": "Heating Target Temperature",
        "icon": "mdi:heating-coil",
        "unit": "°C",
        "min_value": 15.0,
        "max_value": 55.0,
        "step": 1.0,
    },
}

# Select Types - read-write enums
SELECT_TYPES = {
    "mode": {
        "dp_id": 2,
        "code": "mode",
        "name": "Operation Mode",
        "icon": "mdi:hvac",
        "options": {
            "smart": "Smart",
            "strong": "Strong",
            "mute": "Silent",
        },
    },
    "work_mode": {
        "dp_id": 5,
        "code": "work_mode",
        "name": "Work Mode",
        "icon": "mdi:cog",
        "options": {
            "wth": "Hot Water",
            "heat": "Heating",
            "cool": "Cooling",
            "wth_heat": "Hot Water + Heating",
            "wth_cool": "Hot Water + Cooling",
        },
    },
    "temp_unit_convert": {
        "dp_id": 6,
        "code": "temp_unit_convert",
        "name": "Temperature Unit",
        "icon": "mdi:thermometer",
        "options": {
            "c": "Celsius",
            "f": "Fahrenheit",
        },
    },
}
