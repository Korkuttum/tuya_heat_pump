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
        "name": "Current Temperature (Fahrenheit)",
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
        "icon": "mdi:thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
        "conversion": "value"
    },
    "odd_hot_water": {
        "dp_id": 102,
        "code": "odd_hot_water",
        "name": "Remaining Hot Water",
        "unit": "",
        "icon": "mdi:water",
        "state_class": "measurement",
        "conversion": "value"
    },
    "out_air_sensor_temp": {
        "dp_id": 107,
        "code": "out_air_sensor_temp",
        "name": "Exhaust Temperature",
        "unit": "°C",
        "icon": "mdi:thermometer",
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
        "icon": "mdi:thermometer",
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
        "icon": "mdi:sine-wave",
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
        "name": "Set Temperature Lower Limit",
        "unit": "°C",
        "icon": "mdi:thermometer-chevron-down",
        "state_class": "measurement",
        "conversion": "value"
    },
    "set_temp_upper_limit": {
        "dp_id": 122,
        "code": "set_temp_upper_limit",
        "name": "Set Temperature Upper Limit",
        "unit": "°C",
        "icon": "mdi:thermometer-chevron-up",
        "state_class": "measurement",
        "conversion": "value"
    },
}

# ====================================================
# BINARY SENSOR TYPES (read-only boolean)
# ====================================================
BINARY_SENSOR_TYPES = {
    "compressor_status": {
        "dp_id": 103,
        "code": "compressor_status",
        "name": "Compressor Status",
        "device_class": "running",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']"
    },
    "aux_elec_heating_status": {
        "dp_id": 104,
        "code": "aux_elec_heating_status",
        "name": "Auxiliary Electric Heating Status",
        "device_class": "heat",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']"
    },
}

# ====================================================
# SWITCH TYPES (read-write boolean - accessMode: "rw")
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
        "name": "Child Lock",
        "icon": "mdi:lock",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']"
    },
    "silent_heating_status": {
        "dp_id": 106,
        "code": "silent_heating_status",
        "name": "MUTE Mode",
        "icon": "mdi:volume-off",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']"
    },
    "auxiliary_heating_status": {
        "dp_id": 117,
        "code": "auxiliary_heating_status",
        "name": "BOOST Mode",
        "icon": "mdi:rocket-launch",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']"
    },
    "cooling_mode_switch": {
        "dp_id": 118,
        "code": "cooling_mode_switch",
        "name": "Cooling Mode",
        "icon": "mdi:snowflake",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']"
    },
    "cool_mode_lock_status": {
        "dp_id": 120,
        "code": "cool_mode_lock_status",
        "name": "Cooling Mode Lock Status",
        "icon": "mdi:lock",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']"
    },
    "fast_recover": {
        "dp_id": 123,
        "code": "fast_recover",
        "name": "Fast Recovery",
        "icon": "mdi:speedometer",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']"
    },
    "off_peak_period_scheme": {
        "dp_id": 124,
        "code": "off_peak_period_scheme",
        "name": "Week Execution Consistency",
        "icon": "mdi:calendar-clock",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']"
    },
    "lock_device": {
        "dp_id": 125,
        "code": "lock_device",
        "name": "Device Lock",
        "icon": "mdi:lock",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']"
    },
    "checked_status_mon": {
        "dp_id": 186,
        "code": "checked_status_mon",
        "name": "Monday Status",
        "icon": "mdi:calendar",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']"
    },
    "checked_status_tue": {
        "dp_id": 187,
        "code": "checked_status_tue",
        "name": "Tuesday Status",
        "icon": "mdi:calendar",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']"
    },
    "checked_status_wed": {
        "dp_id": 188,
        "code": "checked_status_wed",
        "name": "Wednesday Status",
        "icon": "mdi:calendar",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']"
    },
    "checked_status_thu": {
        "dp_id": 189,
        "code": "checked_status_thu",
        "name": "Thursday Status",
        "icon": "mdi:calendar",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']"
    },
    "checked_status_fri": {
        "dp_id": 190,
        "code": "checked_status_fri",
        "name": "Friday Status",
        "icon": "mdi:calendar",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']"
    },
    "checked_status_sat": {
        "dp_id": 191,
        "code": "checked_status_sat",
        "name": "Saturday Status",
        "icon": "mdi:calendar",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']"
    },
    "checked_status_sun": {
        "dp_id": 192,
        "code": "checked_status_sun",
        "name": "Sunday Status",
        "icon": "mdi:calendar",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']"
    },
}

# ====================================================
# NUMBER TYPES (read-write value - accessMode: "rw")
# ====================================================
NUMBER_TYPES = {
    "temp_set": {
        "dp_id": 4,
        "code": "temp_set",
        "name": "Target Water Temperature",
        "icon": "mdi:thermometer",
        "unit": "°F",  # Model açıklamasında Fahrenheit olduğu belirtilmiş
        "min_value": 0.0,
        "max_value": 176.0,
        "step": 1.0,
        "conversion": "value",
        "api_conversion": "value"
    },
    "mute_start_time": {
        "dp_id": 150,
        "code": "mute_start_time",
        "name": "Mute Heating Start Time",
        "icon": "mdi:timer-play",
        "unit": "minutes",
        "min_value": 0.0,
        "max_value": 1440.0,
        "step": 1.0,
        "conversion": "value",
        "api_conversion": "value"
    },
    "mute_end_time": {
        "dp_id": 151,
        "code": "mute_end_time",
        "name": "Mute Heating End Time",
        "icon": "mdi:timer-stop",
        "unit": "minutes",
        "min_value": 0.0,
        "max_value": 1440.0,
        "step": 1.0,
        "conversion": "value",
        "api_conversion": "value"
    },
}

# ====================================================
# SELECT TYPES (read-write enum - accessMode: "rw")
# ====================================================
SELECT_TYPES = {
    "heating_mode": {
        "dp_id": 105,
        "code": "heating_mode",
        "name": "Mode Selection",
        "icon": "mdi:air-conditioner",
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
        "icon": "mdi:thermometer",
        "options": {
            "0": "Celsius",
            "1": "Fahrenheit"
        },
        "conversion": "value"
    },
}
