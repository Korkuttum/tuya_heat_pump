"""Model mapping for EnviroSun HP+ Tuya Heat Pump."""

MODEL_NAME = "Tuya Heat Pump (EnviroSun HP+)"
# ====================================================
# EnviroSun HP+ @jascham
# ====================================================

SENSOR_TYPES = {
    "temp_current": {
        "dp_id": 16,
        "code": "temp_current",
        "name": "Current Water Temperature",
        "unit": "°C",
        "icon": "mdi:thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
        "conversion": "value"
    },
    "temp_current_f": {
        "dp_id": 35,
        "code": "temp_current_f",
        "name": "Current Temperature (°F)",
        "unit": "°F",
        "icon": "mdi:thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
        "conversion": "value"
    },
    "indoor_sensor_temperature": {
        "dp_id": 101,
        "code": "indoor_sensor_temperature",
        "name": "Ambient Temperature",
        "unit": "°C",
        "icon": "mdi:home-thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
        "conversion": "value"
    },
    "odd_hot_water": {
        "dp_id": 102,
        "code": "odd_hot_water",
        "name": "Remaining Hot Water Volume",
        "unit": "",
        "icon": "mdi:water-percent",
        "state_class": "measurement",
        "conversion": "value"
    },
    "out_air_sensor_temp": {
        "dp_id": 107,
        "code": "out_air_sensor_temp",
        "name": "Exhaust Temperature",
        "unit": "°C",
        "icon": "mdi:thermometer-high",
        "device_class": "temperature",
        "state_class": "measurement",
        "conversion": "value"
    },
    "evap_temperature": {
        "dp_id": 108,
        "code": "evap_temperature",
        "name": "Evaporator Temperature",
        "unit": "°C",
        "icon": "mdi:thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
        "conversion": "value"
    },
    "in_air_sensor_temperature": {
        "dp_id": 109,
        "code": "in_air_sensor_temperature",
        "name": "Suction Temperature",
        "unit": "°C",
        "icon": "mdi:thermometer-low",
        "device_class": "temperature",
        "state_class": "measurement",
        "conversion": "value"
    },
    "fan1_speed": {
        "dp_id": 112,
        "code": "fan1_speed",
        "name": "Fan Speed",
        "unit": "RPM",
        "icon": "mdi:fan",
        "state_class": "measurement",
        "conversion": "value"
    },
    "compressor_frequency": {
        "dp_id": 113,
        "code": "compressor_frequency",
        "name": "Compressor Frequency",
        "unit": "Hz",
        "icon": "mdi:cosine-wave",
        "state_class": "measurement",
        "conversion": "value"
    },
    "software_v_display_board": {
        "dp_id": 114,
        "code": "software_v_display_board",
        "name": "Display Board Software Version",
        "unit": "",
        "icon": "mdi:chip",
        "state_class": "measurement",
        "conversion": "value"
    },
    "software_v_main_board": {
        "dp_id": 115,
        "code": "software_v_main_board",
        "name": "Main Board Software Version",
        "unit": "",
        "icon": "mdi:chip",
        "state_class": "measurement",
        "conversion": "value"
    },
    "cooling_temperature": {
        "dp_id": 116,
        "code": "cooling_temperature",
        "name": "Cooling Temperature",
        "unit": "°C",
        "icon": "mdi:snowflake",
        "device_class": "temperature",
        "state_class": "measurement",
        "conversion": "value"
    },
    "set_temp_lower_limit": {
        "dp_id": 121,
        "code": "set_temp_lower_limit",
        "name": "Set Temperature Min Limit",
        "unit": "°C",
        "icon": "mdi:thermometer-low",
        "device_class": "temperature",
        "state_class": "measurement",
        "conversion": "value"
    },
    "set_temp_upper_limit": {
        "dp_id": 122,
        "code": "set_temp_upper_limit",
        "name": "Set Temperature Max Limit",
        "unit": "°C",
        "icon": "mdi:thermometer-high",
        "device_class": "temperature",
        "state_class": "measurement",
        "conversion": "value"
    },
}

BINARY_SENSOR_TYPES = {
    "switch": {
        "dp_id": 1,
        "code": "switch",
        "name": "Power Switch",
        "device_class": "power",
        "conversion": "value in [True, 1, '1', 'true', 'on', 'yes', 'enable', 'open']"
    },
    "child_lock": {
        "dp_id": 3,
        "code": "child_lock",
        "name": "Child Lock",
        "device_class": "lock",
        "conversion": "value in [True, 1, '1', 'true', 'on', 'yes', 'enable', 'open']"
    },
    "compressor_status": {
        "dp_id": 103,
        "code": "compressor_status",
        "name": "Compressor Running",
        "device_class": "running",
        "conversion": "value in [True, 1, '1', 'true', 'on', 'yes', 'enable', 'open']"
    },
    "aux_elec_heating_status": {
        "dp_id": 104,
        "code": "aux_elec_heating_status",
        "name": "Auxiliary Electric Heating",
        "device_class": "heat",
        "conversion": "value in [True, 1, '1', 'true', 'on', 'yes', 'enable', 'open']"
    },
    "silent_heating_status": {
        "dp_id": 106,
        "code": "silent_heating_status",
        "name": "Mute Mode",
        "device_class": "silent",
        "conversion": "value in [True, 1, '1', 'true', 'on', 'yes', 'enable', 'open']"
    },
    "auxiliary_heating_status": {
        "dp_id": 117,
        "code": "auxiliary_heating_status",
        "name": "Boost Mode",
        "device_class": "heat",
        "conversion": "value in [True, 1, '1', 'true', 'on', 'yes', 'enable', 'open']"
    },
    "cooling_mode_switch": {
        "dp_id": 118,
        "code": "cooling_mode_switch",
        "name": "Cooling Mode",
        "device_class": "snowflake",
        "conversion": "value in [True, 1, '1', 'true', 'on', 'yes', 'enable', 'open']"
    },
    "cool_mode_lock_status": {
        "dp_id": 120,
        "code": "cool_mode_lock_status",
        "name": "Cooling Mode Locked",
        "device_class": "lock",
        "conversion": "value in [True, 1, '1', 'true', 'on', 'yes', 'enable', 'open']"
    },
    "fast_recover": {
        "dp_id": 123,
        "code": "fast_recover",
        "name": "Fast Recovery",
        "device_class": "rocket",
        "conversion": "value in [True, 1, '1', 'true', 'on', 'yes', 'enable', 'open']"
    },
    "off_peak_period_scheme": {
        "dp_id": 124,
        "code": "off_peak_period_scheme",
        "name": "Weekly Schedule Consistent",
        "device_class": "calendar",
        "conversion": "value in [True, 1, '1', 'true', 'on', 'yes', 'enable', 'open']"
    },
    "lock_device": {
        "dp_id": 125,
        "code": "lock_device",
        "name": "Device Lock",
        "device_class": "lock",
        "conversion": "value in [True, 1, '1', 'true', 'on', 'yes', 'enable', 'open']"
    },
}

SWITCH_TYPES = {
    "switch": {
        "dp_id": 1,
        "code": "switch",
        "name": "Power",
        "icon": "mdi:power",
        "conversion": "value in [True, 1, '1', 'true', 'on', 'yes', 'enable', 'open']"
    },
    "child_lock": {
        "dp_id": 3,
        "code": "child_lock",
        "name": "Child Lock",
        "icon": "mdi:lock",
        "conversion": "value in [True, 1, '1', 'true', 'on', 'yes', 'enable', 'open']"
    },
    "silent_heating_status": {
        "dp_id": 106,
        "code": "silent_heating_status",
        "name": "Mute Mode",
        "icon": "mdi:volume-off",
        "conversion": "value in [True, 1, '1', 'true', 'on', 'yes', 'enable', 'open']"
    },
    "cooling_mode_switch": {
        "dp_id": 118,
        "code": "cooling_mode_switch",
        "name": "Cooling Mode",
        "icon": "mdi:snowflake",
        "conversion": "value in [True, 1, '1', 'true', 'on', 'yes', 'enable', 'open']"
    },
    "fast_recover": {
        "dp_id": 123,
        "code": "fast_recover",
        "name": "Fast Recovery",
        "icon": "mdi:rocket-launch",
        "conversion": "value in [True, 1, '1', 'true', 'on', 'yes', 'enable', 'open']"
    },
    "off_peak_period_scheme": {
        "dp_id": 124,
        "code": "off_peak_period_scheme",
        "name": "Weekly Schedule Consistent",
        "icon": "mdi:calendar-check",
        "conversion": "value in [True, 1, '1', 'true', 'on', 'yes', 'enable', 'open']"
    },
    "lock_device": {
        "dp_id": 125,
        "code": "lock_device",
        "name": "Device Lock",
        "icon": "mdi:lock",
        "conversion": "value in [True, 1, '1', 'true', 'on', 'yes', 'enable', 'open']"
    },
}

NUMBER_TYPES = {
    "temp_set": {
        "dp_id": 4,
        "code": "temp_set",
        "name": "Target Water Temperature",
        "icon": "mdi:thermometer",
        "unit": "°C",
        "min_value": 0.0,
        "max_value": 80.0,
        "step": 1.0,
        "conversion": "value",
        "api_conversion": "value"
    },
}

SELECT_TYPES = {
    "heating_mode": {
        "dp_id": 105,
        "code": "heating_mode",
        "name": "Mode Selection",
        "icon": "mdi:heat-pump",
        "options": {
            "0": "Mode 0",
            "1": "Mode 1",
            "2": "Mode 2",
            "3": "Mode 3"
        },
        "conversion": "value"
    },
    "temp_unit": {
        "dp_id": 119,
        "code": "temp_unit",
        "name": "Temperature Unit",
        "icon": "mdi:temperature-celsius",
        "options": {
            "0": "Celsius",
            "1": "Fahrenheit"
        },
        "conversion": "value"
    },
}
