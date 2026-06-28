"""Model mapping for DELLA AC/Heat Pump (e1moeap8)."""

MODEL_NAME = "DELLA AC/Heat Pump (e1moeap8)"
# ====================================================
# DELLA @Chrissica06
# ====================================================
SENSOR_TYPES = {
    "temp_current": {
        "dp_id": 3,
        "code": "temp_current",
        "name": "Current Temperature",
        "unit": "°C",
        "icon": "mdi:thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
        "conversion": "value / 100"
    },
    "ure": {
        "dp_id": 116,
        "code": "ure",
        "name": "Outdoor Temperature",
        "unit": "°C",
        "icon": "mdi:thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
        "conversion": "value / 100"
    },
    "upper_tem_limit": {
        "dp_id": 113,
        "code": "upper_tem_limit",
        "name": "Temperature Upper Limit",
        "unit": "°C",
        "icon": "mdi:thermometer-chevron-up",
        "device_class": "temperature",
        "state_class": "measurement",
        "conversion": "value / 100"
    },
    "lower_tem_limit": {
        "dp_id": 114,
        "code": "lower_tem_limit",
        "name": "Temperature Lower Limit",
        "unit": "°C",
        "icon": "mdi:thermometer-chevron-down",
        "device_class": "temperature",
        "state_class": "measurement",
        "conversion": "value / 100"
    },
    "external_unit_fanspeed": {
        "dp_id": 117,
        "code": "external_unit_fanspeed",
        "name": "Outdoor Fan Speed",
        "unit": "rpm",
        "icon": "mdi:fan",
        "state_class": "measurement",
    },
    "compressor_frequency": {
        "dp_id": 119,
        "code": "compressor_frequency",
        "name": "Compressor Frequency",
        "unit": "Hz",
        "icon": "mdi:sine-wave",
        "state_class": "measurement",
    },
    "outdoor_comptar_freqrun": {
        "dp_id": 120,
        "code": "outdoor_comptar_freqrun",
        "name": "Outdoor Compressor Target Frequency",
        "unit": "Hz",
        "icon": "mdi:sine-wave",
        "state_class": "measurement",
    },
    "electricity": {
        "dp_id": 127,
        "code": "electricity",
        "name": "Electricity Consumption",
        "unit": "kWh",
        "icon": "mdi:lightning-bolt",
        "device_class": "energy",
        "state_class": "total_increasing",
        "conversion": "value / 100"
    },
    "wind_speed_percentage": {
        "dp_id": 115,
        "code": "wind_speed_percentage",
        "name": "Wind Speed Percentage",
        "unit": "%",
        "icon": "mdi:fan",
        "state_class": "measurement",
    },
}

# ====================================================
# BINARY SENSOR TYPES (read-only boolean)
# ====================================================
BINARY_SENSOR_TYPES = {
    "heat_status": {
        "dp_id": 103,
        "code": "heat_status",
        "name": "Electric Heater Status",
        "device_class": "heat",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']"
    },
    "freshair_status": {
        "dp_id": 108,
        "code": "freshair_status",
        "name": "Fresh Air Filter Block Status",
        "device_class": "problem",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']"
    },
    "filter_block_status": {
        "dp_id": 110,
        "code": "filter_block_status",
        "name": "Filter Block Status",
        "device_class": "problem",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']"
    },
    "access_card_insert": {
        "dp_id": 112,
        "code": "access_card_insert",
        "name": "Access Card Inserted",
        "device_class": "plug",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']"
    },
    "examine_mode": {
        "dp_id": 144,
        "code": "examine_mode",
        "name": "Examine Mode",
        "device_class": "running",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']"
    },
    "stores_mode": {
        "dp_id": 145,
        "code": "stores_mode",
        "name": "Store Display Mode",
        "device_class": "running",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']"
    },
    "light_senser_status": {
        "dp_id": 156,
        "code": "light_senser_status",
        "name": "Light Sensor Status",
        "device_class": "light",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']"
    },
    "filter_blocknotify": {
        "dp_id": 149,
        "code": "filter_blocknotify",
        "name": "Filter Block Notification",
        "device_class": "problem",
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
    "auto": {
        "dp_id": 7,
        "code": "auto",
        "name": "Fan Speed Auto",
        "icon": "mdi:fan-auto",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']"
    },
    "eco": {
        "dp_id": 8,
        "code": "eco",
        "name": "ECO Mode",
        "icon": "mdi:leaf",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']"
    },
    "drying": {
        "dp_id": 9,
        "code": "drying",
        "name": "Drying",
        "icon": "mdi:water-off",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']"
    },
    "heat": {
        "dp_id": 12,
        "code": "heat",
        "name": "Electric Heater",
        "icon": "mdi:radiator",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']"
    },
    "light": {
        "dp_id": 13,
        "code": "light",
        "name": "Display Light",
        "icon": "mdi:lightbulb",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']"
    },
    "beep": {
        "dp_id": 16,
        "code": "beep",
        "name": "Beep Sound",
        "icon": "mdi:volume-high",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']"
    },
    "health": {
        "dp_id": 26,
        "code": "health",
        "name": "Health Mode",
        "icon": "mdi:heart-pulse",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']"
    },
    "cleaning": {
        "dp_id": 27,
        "code": "cleaning",
        "name": "Self Clean",
        "icon": "mdi:vacuum",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']"
    },
    "fresh_air_valve": {
        "dp_id": 39,
        "code": "fresh_air_valve",
        "name": "Fresh Air Valve",
        "icon": "mdi:air-filter",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']"
    },
    "temperature_type": {
        "dp_id": 101,
        "code": "temperature_type",
        "name": "Fahrenheit Mode",
        "icon": "mdi:temperature-fahrenheit",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']"
    },
    "eight_add_hot": {
        "dp_id": 102,
        "code": "eight_add_hot",
        "name": "8°C Heating",
        "icon": "mdi:snowflake-thermometer",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']"
    },
    "high_temperature_wind": {
        "dp_id": 104,
        "code": "high_temperature_wind",
        "name": "High Temperature Wind",
        "icon": "mdi:weather-windy",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']"
    },
    "cool_feel_wind": {
        "dp_id": 105,
        "code": "cool_feel_wind",
        "name": "Cool Feel Wind",
        "icon": "mdi:snowflake",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']"
    },
    "new_wind_auto_switch": {
        "dp_id": 106,
        "code": "new_wind_auto_switch",
        "name": "Fresh Air Auto",
        "icon": "mdi:air-filter",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']"
    },
    "ai_eco_switch": {
        "dp_id": 111,
        "code": "ai_eco_switch",
        "name": "AI ECO Mode",
        "icon": "mdi:robot",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']"
    },
    "light_sense": {
        "dp_id": 135,
        "code": "light_sense",
        "name": "Light Sensor",
        "icon": "mdi:brightness-auto",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']"
    },
    "voice_switch": {
        "dp_id": 142,
        "code": "voice_switch",
        "name": "Voice Control",
        "icon": "mdi:microphone",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']"
    },
    "newwind_super": {
        "dp_id": 155,
        "code": "newwind_super",
        "name": "Fresh Air Super Wind",
        "icon": "mdi:weather-windy",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']"
    },
    "proximity_senseswitch": {
        "dp_id": 158,
        "code": "proximity_senseswitch",
        "name": "Proximity Sensor",
        "icon": "mdi:motion-sensor",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']"
    },
    "openadr_switch": {
        "dp_id": 160,
        "code": "openadr_switch",
        "name": "OpenADR Switch",
        "icon": "mdi:transmission-tower",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']"
    },
}

# ====================================================
# NUMBER TYPES (read-write value - accessMode: "rw")
# ====================================================
NUMBER_TYPES = {
    "temp_set": {
        "dp_id": 2,
        "code": "temp_set",
        "name": "Target Temperature",
        "icon": "mdi:thermometer",
        "unit": "°C",
        "min_value": 16.0,
        "max_value": 31.0,
        "step": 0.5,
        "conversion": "value / 100",
        "api_conversion": "value * 100"
    },
    "temp_set_f": {
        "dp_id": 24,
        "code": "temp_set_f",
        "name": "Target Temperature (Fahrenheit)",
        "icon": "mdi:thermometer",
        "unit": "°F",
        "min_value": 61.0,
        "max_value": 88.0,
        "step": 1.0,
        "api_conversion": "value"
    },
    "volume": {
        "dp_id": 141,
        "code": "volume",
        "name": "Voice Volume",
        "icon": "mdi:volume-medium",
        "unit": "%",
        "min_value": 10.0,
        "max_value": 100.0,
        "step": 1.0,
        "api_conversion": "value"
    },
    "outdoor_fan_tarspeed": {
        "dp_id": 118,
        "code": "outdoor_fan_tarspeed",
        "name": "Outdoor Fan Target Speed",
        "icon": "mdi:fan",
        "unit": "",
        "min_value": 0.0,
        "max_value": 200.0,
        "step": 1.0,
        "api_conversion": "value"
    },
    "outdoor_comptar_freqset": {
        "dp_id": 121,
        "code": "outdoor_comptar_freqset",
        "name": "Outdoor Compressor Frequency Set",
        "icon": "mdi:sine-wave",
        "unit": "Hz",
        "min_value": 0.0,
        "max_value": 150.0,
        "step": 1.0,
        "api_conversion": "value"
    },
    "outdoor_eevtar_opendegree": {
        "dp_id": 122,
        "code": "outdoor_eevtar_opendegree",
        "name": "Outdoor EEV Open Degree",
        "icon": "mdi:pipe-valve",
        "unit": "",
        "min_value": 0.0,
        "max_value": 500.0,
        "step": 1.0,
        "api_conversion": "value"
    },
}

# ====================================================
# SELECT TYPES (read-write enum - accessMode: "rw")
# ====================================================
SELECT_TYPES = {
    "mode": {
        "dp_id": 4,
        "code": "mode",
        "name": "Operation Mode",
        "icon": "mdi:hvac",
        "options": {
            "0": "Auto",
            "1": "Cool",
            "2": "Dehumidify",
            "3": "Fan Only",
            "4": "Heat",
            "11": "Auxiliary Heat"
        },
    },
    "fan_speed_enum": {
        "dp_id": 5,
        "code": "fan_speed_enum",
        "name": "Fan Speed",
        "icon": "mdi:fan",
        "options": {
            "0": "Stop",
            "1": "Silent",
            "2": "Low",
            "3": "Medium Low",
            "4": "Medium",
            "5": "Medium High",
            "6": "High",
            "7": "Turbo"
        },
    },
    "gear_vertical": {
        "dp_id": 31,
        "code": "gear_vertical",
        "name": "Vertical Vane Position",
        "icon": "mdi:arrow-up-down",
        "options": {
            "1": "Swing Up/Down",
            "2": "Blow Up",
            "3": "Blow Down",
            "6": "Surround",
            "8": "Fixed Position",
            "9": "Top Fixed",
            "10": "Upper Fixed",
            "11": "Middle Fixed",
            "12": "Lower Fixed",
            "13": "Bottom Fixed"
        },
    },
    "gear_horizontal": {
        "dp_id": 34,
        "code": "gear_horizontal",
        "name": "Horizontal Vane Position",
        "icon": "mdi:arrow-left-right",
        "options": {
            "1": "Swing Left/Right",
            "2": "Blow Left",
            "3": "Blow Center",
            "4": "Blow Right",
            "5": "Blow Both Sides",
            "8": "Fixed Position",
            "9": "Left Fixed",
            "10": "Left-Center Fixed",
            "11": "Center Fixed",
            "12": "Right-Center Fixed",
            "13": "Right Fixed",
            "17": "Surround"
        },
    },
    "vertical_wind": {
        "dp_id": 137,
        "code": "vertical_wind",
        "name": "Vertical Swing",
        "icon": "mdi:arrow-up-down-bold",
        "options": {
            "0": "Off",
            "1": "On"
        },
    },
    "horizontal_wind": {
        "dp_id": 138,
        "code": "horizontal_wind",
        "name": "Horizontal Swing",
        "icon": "mdi:arrow-left-right-bold",
        "options": {
            "0": "Off",
            "1": "On"
        },
    },
    "supply_fan_speed": {
        "dp_id": 40,
        "code": "supply_fan_speed",
        "name": "Fresh Air Fan Speed",
        "icon": "mdi:fan",
        "options": {
            "0": "Stop",
            "1": "Low",
            "2": "Medium",
            "3": "High"
        },
    },
    "sleep_enum": {
        "dp_id": 126,
        "code": "sleep_enum",
        "name": "Sleep Mode",
        "icon": "mdi:sleep",
        "options": {
            "0": "Off",
            "1": "Standard",
            "2": "Elderly",
            "3": "Child"
        },
    },
    "soft_wind": {
        "dp_id": 123,
        "code": "soft_wind",
        "name": "Soft Wind",
        "icon": "mdi:weather-windy-variant",
        "options": {
            "0": "Off",
            "1": "On"
        },
    },
    "generator_mode": {
        "dp_id": 132,
        "code": "generator_mode",
        "name": "Generator Mode",
        "icon": "mdi:engine",
        "options": {
            "0": "Off",
            "1": "Level 1",
            "2": "Level 2",
            "3": "Level 3",
            "4": "Level 4",
            "5": "Level 5",
            "6": "Level 6"
        },
    },
    "smart_windmode": {
        "dp_id": 147,
        "code": "smart_windmode",
        "name": "Smart Wind Mode",
        "icon": "mdi:robot",
        "options": {
            "0": "Off",
            "1": "Avoid People",
            "2": "Follow People"
        },
    },
}
