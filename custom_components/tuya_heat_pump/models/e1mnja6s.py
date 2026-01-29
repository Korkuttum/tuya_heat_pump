"""Model mapping for EnviroSun HP+ Tuya Heat Pump."""

MODEL_NAME = "Tuya Heat Pump (EnviroSun HP+)"
# ====================================================
# EnviroSun HP+ @jascham
# ====================================================
# Raw DP'ler (eco_mode zamanları, gr_set_*) hariç tutuldu.

SENSOR_TYPES = {
    "temp_current": {
        "dp_id": 16,
        "code": "temp_current",
        "name": "Current Temperature",
        "unit": "°C",
        "icon": "mdi:thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
        "conversion": "value"   # Eğer değerler 10 kat büyük gelirse → "value / 10" yap
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
        "name": "Indoor Sensor Temperature",
        "unit": "°C",
        "icon": "mdi:home-thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
        "conversion": "value"
    },
    "odd_hot_water": {
        "dp_id": 102,
        "code": "odd_hot_water",
        "name": "Odd Hot Water / Mode Related Value",
        "unit": "",
        "icon": "mdi:water-thermometer-outline",
        "state_class": "measurement",
        "conversion": "value"
    },
    "out_air_sensor_temp": {
        "dp_id": 107,
        "code": "out_air_sensor_temp",
        "name": "Outdoor Air Sensor Temperature",
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
        "name": "Indoor Air Sensor Temperature",
        "unit": "°C",
        "icon": "mdi:thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
        "conversion": "value"
    },
    "fan1_speed": {
        "dp_id": 112,
        "code": "fan1_speed",
        "name": "Fan 1 Speed",
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
        "name": "Set Temperature Lower Limit",
        "unit": "°C",
        "icon": "mdi:thermometer-low",
        "device_class": "temperature",
        "state_class": "measurement",
        "conversion": "value"
    },
    "set_temp_upper_limit": {
        "dp_id": 122,
        "code": "set_temp_upper_limit",
        "name": "Set Temperature Upper Limit",
        "unit": "°C",
        "icon": "mdi:thermometer-high",
        "device_class": "temperature",
        "state_class": "measurement",
        "conversion": "value"
    },
}

BINARY_SENSOR_TYPES = {
    "switch": {  # Power aslında switch ama binary olarak da takip edilebilir
        "dp_id": 1,
        "code": "switch",
        "name": "Power Status",
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
        "name": "Silent Heating Active",
        "device_class": "silent",
        "conversion": "value in [True, 1, '1', 'true', 'on', 'yes', 'enable', 'open']"
    },
    "auxiliary_heating_status": {
        "dp_id": 117,
        "code": "auxiliary_heating_status",
        "name": "Auxiliary Heating",
        "device_class": "heat",
        "conversion": "value in [True, 1, '1', 'true', 'on', 'yes', 'enable', 'open']"
    },
    "cooling_mode_switch": {
        "dp_id": 118,
        "code": "cooling_mode_switch",
        "name": "Cooling Mode Active",
        "device_class": "snowflake",
        "conversion": "value in [True, 1, '1', 'true', 'on', 'yes', 'enable', 'open']"
    },
    "cool_mode_lock_status": {
        "dp_id": 120,
        "code": "cool_mode_lock_status",
        "name": "Cool Mode Locked",
        "device_class": "lock",
        "conversion": "value in [True, 1, '1', 'true', 'on', 'yes', 'enable', 'open']"
    },
    "fast_recover": {
        "dp_id": 123,
        "code": "fast_recover",
        "name": "Fast Recovery Mode",
        "device_class": "rocket",
        "conversion": "value in [True, 1, '1', 'true', 'on', 'yes', 'enable', 'open']"
    },
    "off_peak_period_scheme": {
        "dp_id": 124,
        "code": "off_peak_period_scheme",
        "name": "Off-Peak Period Enabled",
        "device_class": "clock",
        "conversion": "value in [True, 1, '1', 'true', 'on', 'yes', 'enable', 'open']"
    },
    "lock_device": {
        "dp_id": 125,
        "code": "lock_device",
        "name": "Device Locked",
        "device_class": "lock",
        "conversion": "value in [True, 1, '1', 'true', 'on', 'yes', 'enable', 'open']"
    },
    # Haftalık program günleri
    "checked_status_mon": {
        "dp_id": 162,  # txt'deki sıraya göre yaklaşık, doğrulayın
        "code": "checked_status_mon",
        "name": "Schedule Monday",
        "device_class": "calendar",
        "conversion": "value in [True, 1, '1', 'true', 'on', 'yes', 'enable', 'open']"
    },
    "checked_status_tue": {
        "dp_id": 163,
        "code": "checked_status_tue",
        "name": "Schedule Tuesday",
        "device_class": "calendar",
        "conversion": "value in [True, 1, '1', 'true', 'on', 'yes', 'enable', 'open']"
    },
    "checked_status_wed": {
        "dp_id": 164,
        "code": "checked_status_wed",
        "name": "Schedule Wednesday",
        "device_class": "calendar",
        "conversion": "value in [True, 1, '1', 'true', 'on', 'yes', 'enable', 'open']"
    },
    "checked_status_thu": {
        "dp_id": 165,
        "code": "checked_status_thu",
        "name": "Schedule Thursday",
        "device_class": "calendar",
        "conversion": "value in [True, 1, '1', 'true', 'on', 'yes', 'enable', 'open']"
    },
    "checked_status_fri": {
        "dp_id": 166,
        "code": "checked_status_fri",
        "name": "Schedule Friday",
        "device_class": "calendar",
        "conversion": "value in [True, 1, '1', 'true', 'on', 'yes', 'enable', 'open']"
    },
    "checked_status_sat": {
        "dp_id": 167,
        "code": "checked_status_sat",
        "name": "Schedule Saturday",
        "device_class": "calendar",
        "conversion": "value in [True, 1, '1', 'true', 'on', 'yes', 'enable', 'open']"
    },
    "checked_status_sun": {
        "dp_id": 168,
        "code": "checked_status_sun",
        "name": "Schedule Sunday",
        "device_class": "calendar",
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
        "name": "Fast Recover",
        "icon": "mdi:rocket-launch",
        "conversion": "value in [True, 1, '1', 'true', 'on', 'yes', 'enable', 'open']"
    },
    "off_peak_period_scheme": {
        "dp_id": 124,
        "code": "off_peak_period_scheme",
        "name": "Off-Peak Scheme",
        "icon": "mdi:clock-outline",
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
        "name": "Temperature Setpoint",
        "icon": "mdi:thermometer",
        "unit": "°C",
        "min_value": 5.0,
        "max_value": 80.0,
        "step": 1.0,
        "conversion": "value",
        "api_conversion": "value"
    },
    "cooling_temperature": {
        "dp_id": 116,
        "code": "cooling_temperature",
        "name": "Cooling Temperature Set",
        "icon": "mdi:snowflake-thermometer",
        "unit": "°C",
        "min_value": 5.0,
        "max_value": 40.0,   # Tahmini, cihazınıza göre değiştirin
        "step": 1.0,
        "conversion": "value",
        "api_conversion": "value"
    },
}

SELECT_TYPES = {
    "heating_mode": {
        "dp_id": 105,
        "code": "heating_mode",
        "name": "Heating Mode",
        "icon": "mdi:heat-pump",
        "options": {
            "0": "Off / Standby",   # Gerçek seçenekleri Tuya app veya log'dan doğrula
            "1": "Heating",
            "2": "Cooling",
            "3": "Auto",
            # Daha fazla varsa ekleyin
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
