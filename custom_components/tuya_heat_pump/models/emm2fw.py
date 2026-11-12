# ====================================================
# Rakentaa RA040-PW13-A3 @cpiekacz, issue #116
# Tuya modelId: emm2fw
# Inverter air-to-water heat pump with enhanced vapour injection
# (EVI), hot water tank and heating / cooling.
#
# Every plain DP of the cloud schema is mapped. NOT mapped:
#   - parameter_group_1 ... parameter_group_7 (dp 118-124): raw
#     blocks that carry the unit's settings (target temperatures,
#     defrost and fan parameters, ...). They have to be decoded
#     with the raw explorer before they can be used, so the
#     target temperatures are not available yet.
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
