"""Model mapping for ACIQ Heat Pump (e1kynud8)."""

MODEL_NAME = "ACIQ Heat Pump (e1kynud8)"
# ====================================================
# ACIQ @wlatic
# ====================================================

# ====================================================
# SENSOR TYPES (read-only value - accessMode: "ro")
# ====================================================
SENSOR_TYPES = {
    # Current Temperature (dp_id: 3) - scale: 2 (value / 100)
    "temp_current": {
        "dp_id": 3,
        "code": "temp_current",
        "name": "Current Temperature",
        "unit": "°C",
        "icon": "mdi:thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
        "conversion": "value / 100",
    },
    # Outdoor Ambient Temperature (dp_id: 116) - scale: 2 (value / 100)
    "ure": {
        "dp_id": 116,
        "code": "ure",
        "name": "Outdoor Temperature",
        "unit": "°C",
        "icon": "mdi:thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
        "conversion": "value / 100",
    },
    # Outdoor Fan Speed (dp_id: 117)
    "external_unit_fanspeed": {
        "dp_id": 117,
        "code": "external_unit_fanspeed",
        "name": "Outdoor Fan Speed",
        "unit": "RPM",
        "icon": "mdi:fan",
        "state_class": "measurement",
    },
    # Compressor Frequency (dp_id: 119)
    "compressor_frequency": {
        "dp_id": 119,
        "code": "compressor_frequency",
        "name": "Compressor Frequency",
        "unit": "Hz",
        "icon": "mdi:sine-wave",
        "state_class": "measurement",
    },
    # Outdoor Compressor Target Frequency (dp_id: 120)
    "outdoor_comptar_freqrun": {
        "dp_id": 120,
        "code": "outdoor_comptar_freqrun",
        "name": "Outdoor Compressor Target Frequency",
        "unit": "Hz",
        "icon": "mdi:sine-wave",
        "state_class": "measurement",
    },
    # Temperature Upper Limit (dp_id: 113) - scale: 2 (value / 100)
    "upper_tem_limit": {
        "dp_id": 113,
        "code": "upper_tem_limit",
        "name": "Temperature Upper Limit",
        "unit": "°C",
        "icon": "mdi:thermometer-chevron-up",
        "device_class": "temperature",
        "state_class": "measurement",
        "conversion": "value / 100",
    },
    # Temperature Lower Limit (dp_id: 114) - scale: 2 (value / 100)
    "lower_tem_limit": {
        "dp_id": 114,
        "code": "lower_tem_limit",
        "name": "Temperature Lower Limit",
        "unit": "°C",
        "icon": "mdi:thermometer-chevron-down",
        "device_class": "temperature",
        "state_class": "measurement",
        "conversion": "value / 100",
    },
    # Electricity (dp_id: 127) - scale: 2 (value / 100)
    "electricity": {
        "dp_id": 127,
        "code": "electricity",
        "name": "Electricity Consumption",
        "unit": "kWh",
        "icon": "mdi:flash",
        "device_class": "energy",
        "state_class": "total_increasing",
        "conversion": "value / 100",
    },
    # Electricity Start Time (dp_id: 128)
    "electricity_starttime": {
        "dp_id": 128,
        "code": "electricity_starttime",
        "name": "Electricity Start Time",
        "unit": "s",
        "icon": "mdi:timer",
        "state_class": "measurement",
    },
    # Electricity End Time (dp_id: 129)
    "electricity_endtime": {
        "dp_id": 129,
        "code": "electricity_endtime",
        "name": "Electricity End Time",
        "unit": "s",
        "icon": "mdi:timer",
        "state_class": "measurement",
    },
    # Solar Power (dp_id: 165)
    "solar_power": {
        "dp_id": 165,
        "code": "solar_power",
        "name": "Solar Input Power",
        "unit": "W",
        "icon": "mdi:solar-power",
        "device_class": "power",
        "state_class": "measurement",
    },
    # Grid Power (dp_id: 166)
    "grid_power": {
        "dp_id": 166,
        "code": "grid_power",
        "name": "Grid Input Power",
        "unit": "W",
        "icon": "mdi:power-plug",
        "device_class": "power",
        "state_class": "measurement",
    },
    # Solar Electricity (dp_id: 167) - scale: 2 (value / 100)
    "solar_electricity": {
        "dp_id": 167,
        "code": "solar_electricity",
        "name": "Solar Electricity",
        "unit": "kWh",
        "icon": "mdi:solar-power",
        "device_class": "energy",
        "state_class": "total_increasing",
        "conversion": "value / 100",
    },
    # AI Energy Saving Time (dp_id: 195)
    "virtual_ai_time": {
        "dp_id": 195,
        "code": "virtual_ai_time",
        "name": "AI Energy Saving Time",
        "unit": "s",
        "icon": "mdi:timer",
        "state_class": "measurement",
    },
    # AI Energy Saving (dp_id: 196) - scale: 2 (value / 100)
    "virtual_ai_save": {
        "dp_id": 196,
        "code": "virtual_ai_save",
        "name": "AI Energy Saving",
        "unit": "kWh",
        "icon": "mdi:leaf",
        "device_class": "energy",
        "state_class": "total_increasing",
        "conversion": "value / 100",
    },
}

# ====================================================
# BINARY SENSOR TYPES (read-only bool - accessMode: "ro")
# ====================================================
BINARY_SENSOR_TYPES = {
    # Electric Heating Status (dp_id: 103)
    "heat_status": {
        "dp_id": 103,
        "code": "heat_status",
        "name": "Electric Heating Status",
        "device_class": "heat",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']",
    },
    # Fresh Air Blocked Status (dp_id: 108)
    "freshair_status": {
        "dp_id": 108,
        "code": "freshair_status",
        "name": "Fresh Air Blocked",
        "device_class": "problem",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']",
    },
    # Filter Blocked Status (dp_id: 110)
    "filter_block_status": {
        "dp_id": 110,
        "code": "filter_block_status",
        "name": "Filter Blocked",
        "device_class": "problem",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']",
    },
    # Access Card Inserted (dp_id: 112)
    "access_card_insert": {
        "dp_id": 112,
        "code": "access_card_insert",
        "name": "Access Card Inserted",
        "device_class": "presence",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']",
    },
    # Light Sensor Status (dp_id: 156)
    "light_senser_status": {
        "dp_id": 156,
        "code": "light_senser_status",
        "name": "Light Sensor Status",
        "device_class": "light",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']",
    },
}

# ====================================================
# SWITCH TYPES (read-write bool - accessMode: "rw")
# ====================================================
SWITCH_TYPES = {
    # Power Switch (dp_id: 1)
    "switch": {
        "dp_id": 1,
        "code": "switch",
        "name": "Power",
        "icon": "mdi:power",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']",
    },
    # Auto Fan Speed (dp_id: 7)
    "auto": {
        "dp_id": 7,
        "code": "auto",
        "name": "Auto Fan Speed",
        "icon": "mdi:fan-auto",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']",
    },
    # ECO Mode (dp_id: 8)
    "eco": {
        "dp_id": 8,
        "code": "eco",
        "name": "ECO Mode",
        "icon": "mdi:leaf",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']",
    },
    # Drying (dp_id: 9)
    "drying": {
        "dp_id": 9,
        "code": "drying",
        "name": "Drying",
        "icon": "mdi:water",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']",
    },
    # Electric Heating (dp_id: 12)
    "heat": {
        "dp_id": 12,
        "code": "heat",
        "name": "Electric Heating",
        "icon": "mdi:heating-coil",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']",
    },
    # Light (dp_id: 13)
    "light": {
        "dp_id": 13,
        "code": "light",
        "name": "Light",
        "icon": "mdi:lightbulb",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']",
    },
    # Beeper (dp_id: 16)
    "beep": {
        "dp_id": 16,
        "code": "beep",
        "name": "Beeper",
        "icon": "mdi:volume-high",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']",
    },
    # Health Mode (dp_id: 26)
    "health": {
        "dp_id": 26,
        "code": "health",
        "name": "Health Mode",
        "icon": "mdi:heart-pulse",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']",
    },
    # Cleaning (dp_id: 27)
    "cleaning": {
        "dp_id": 27,
        "code": "cleaning",
        "name": "Evaporator Cleaning",
        "icon": "mdi:spray",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']",
    },
    # Fresh Air Valve (dp_id: 39)
    "fresh_air_valve": {
        "dp_id": 39,
        "code": "fresh_air_valve",
        "name": "Fresh Air Valve",
        "icon": "mdi:air-filter",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']",
    },
    # Temperature Type (dp_id: 101)
    "temperature_type": {
        "dp_id": 101,
        "code": "temperature_type",
        "name": "Temperature Unit",
        "icon": "mdi:thermometer",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']",
        "options": {
            False: "Celsius",
            True: "Fahrenheit",
        },
    },
    # 8 Degree Heating (dp_id: 102)
    "eight_add_hot": {
        "dp_id": 102,
        "code": "eight_add_hot",
        "name": "8°C Heating",
        "icon": "mdi:thermometer",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']",
    },
    # High Temperature Wind (dp_id: 104)
    "high_temperature_wind": {
        "dp_id": 104,
        "code": "high_temperature_wind",
        "name": "High Temperature Wind",
        "icon": "mdi:weather-sunny",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']",
    },
    # Cool Feel Wind (dp_id: 105)
    "cool_feel_wind": {
        "dp_id": 105,
        "code": "cool_feel_wind",
        "name": "Cool Feel Wind",
        "icon": "mdi:snowflake",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']",
    },
    # Fresh Air Auto Switch (dp_id: 106)
    "new_wind_auto_switch": {
        "dp_id": 106,
        "code": "new_wind_auto_switch",
        "name": "Fresh Air Auto Switch",
        "icon": "mdi:air-filter",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']",
    },
    # AI ECO Switch (dp_id: 111)
    "ai_eco_switch": {
        "dp_id": 111,
        "code": "ai_eco_switch",
        "name": "AI ECO Switch",
        "icon": "mdi:leaf",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']",
    },
    # Light Sense (dp_id: 135)
    "light_sense": {
        "dp_id": 135,
        "code": "light_sense",
        "name": "Light Sense",
        "icon": "mdi:light-sensor",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']",
    },
    # Voice Switch (dp_id: 142)
    "voice_switch": {
        "dp_id": 142,
        "code": "voice_switch",
        "name": "Voice Control",
        "icon": "mdi:microphone",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']",
    },
    # Anti Direct Blow (dp_id: 157)
    "anti_directblow": {
        "dp_id": 157,
        "code": "anti_directblow",
        "name": "Anti Direct Blow",
        "icon": "mdi:wind-turbine",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']",
    },
    # Wide Area Wind (dp_id: 158)
    "widearea_wind": {
        "dp_id": 158,
        "code": "widearea_wind",
        "name": "Wide Area Wind",
        "icon": "mdi:fan",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']",
    },
    # Encircle Wind (dp_id: 159)
    "encircle_wind": {
        "dp_id": 159,
        "code": "encircle_wind",
        "name": "Encircle Wind",
        "icon": "mdi:fan",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']",
    },
    # Zone Wind (dp_id: 160)
    "zone_wind": {
        "dp_id": 160,
        "code": "zone_wind",
        "name": "Zone Wind",
        "icon": "mdi:fan",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']",
    },
    # 3D Wind Switch (dp_id: 163)
    "wind3d_switch": {
        "dp_id": 163,
        "code": "wind3d_switch",
        "name": "3D Wind",
        "icon": "mdi:fan",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']",
    },
    # ADR Switch (dp_id: 170)
    "openadr_switch": {
        "dp_id": 170,
        "code": "openadr_switch",
        "name": "ADR Switch",
        "icon": "mdi:power-settings",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']",
    },
    # ADR Status (dp_id: 171)
    "openadr_status": {
        "dp_id": 171,
        "code": "openadr_status",
        "name": "ADR Status",
        "icon": "mdi:power-settings",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']",
    },
    # New Wind Super (dp_id: 155)
    "newwind_super": {
        "dp_id": 155,
        "code": "newwind_super",
        "name": "Fresh Air Super",
        "icon": "mdi:air-filter",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']",
    },
}

# ====================================================
# NUMBER TYPES (read-write value - accessMode: "rw")
# ====================================================
NUMBER_TYPES = {
    # Target Temperature (dp_id: 2) - scale: 2
    "temp_set": {
        "dp_id": 2,
        "code": "temp_set",
        "name": "Target Temperature",
        "icon": "mdi:thermostat",
        "unit": "°C",
        "min_value": 16.0,
        "max_value": 31.0,
        "step": 0.5,
        "conversion": "value / 100",
        "api_conversion": "value * 100",
    },
    # Target Fahrenheit Temperature (dp_id: 24)
    "temp_set_f": {
        "dp_id": 24,
        "code": "temp_set_f",
        "name": "Target Temperature (F)",
        "icon": "mdi:thermostat",
        "unit": "°F",
        "min_value": 61.0,
        "max_value": 88.0,
        "step": 1.0,
        "api_conversion": "value",
    },
    # Wind Speed Percentage (dp_id: 115)
    "wind_speed_percentage": {
        "dp_id": 115,
        "code": "wind_speed_percentage",
        "name": "Wind Speed Percentage",
        "icon": "mdi:fan",
        "unit": "%",
        "min_value": 0.0,
        "max_value": 100.0,
        "step": 1.0,
        "api_conversion": "value",
    },
    # Outdoor Fan Target Speed (dp_id: 118)
    "outdoor_fan_tarspeed": {
        "dp_id": 118,
        "code": "outdoor_fan_tarspeed",
        "name": "Outdoor Fan Target Speed",
        "icon": "mdi:fan",
        "unit": "",
        "min_value": 0.0,
        "max_value": 200.0,
        "step": 1.0,
        "api_conversion": "value",
    },
    # Outdoor Compressor Target Frequency Set (dp_id: 121)
    "outdoor_comptar_freqset": {
        "dp_id": 121,
        "code": "outdoor_comptar_freqset",
        "name": "Compressor Target Frequency",
        "icon": "mdi:sine-wave",
        "unit": "Hz",
        "min_value": 0.0,
        "max_value": 150.0,
        "step": 1.0,
        "api_conversion": "value",
    },
    # Outdoor EEV Target Opening (dp_id: 122)
    "outdoor_eevtar_opendegree": {
        "dp_id": 122,
        "code": "outdoor_eevtar_opendegree",
        "name": "Outdoor EEV Target Opening",
        "icon": "mdi:pipe-valve",
        "unit": "",
        "min_value": 0.0,
        "max_value": 500.0,
        "step": 1.0,
        "api_conversion": "value",
    },
    # Volume (dp_id: 141)
    "volume": {
        "dp_id": 141,
        "code": "volume",
        "name": "Volume",
        "icon": "mdi:volume-high",
        "unit": "",
        "min_value": 10.0,
        "max_value": 100.0,
        "step": 1.0,
        "api_conversion": "value",
    },
    # Clear Electricity Start Time (dp_id: 130)
    "clearele_starttime": {
        "dp_id": 130,
        "code": "clearele_starttime",
        "name": "Clear Electricity Start Time",
        "icon": "mdi:timer",
        "unit": "s",
        "min_value": 0.0,
        "max_value": 2147483647.0,
        "step": 1.0,
        "api_conversion": "value",
    },
    # Clear Electricity End Time (dp_id: 131)
    "clearele_endtime": {
        "dp_id": 131,
        "code": "clearele_endtime",
        "name": "Clear Electricity End Time",
        "icon": "mdi:timer",
        "unit": "s",
        "min_value": 0.0,
        "max_value": 2147483647.0,
        "step": 1.0,
        "api_conversion": "value",
    },
}

# ====================================================
# SELECT TYPES (read-write enum - accessMode: "rw")
# ====================================================
SELECT_TYPES = {
    # Mode (dp_id: 4)
    "mode": {
        "dp_id": 4,
        "code": "mode",
        "name": "Mode",
        "icon": "mdi:hvac",
        "options": {
            "0": "Auto",
            "1": "Cooling",
            "2": "Dehumidify",
            "3": "Fan Only",
            "4": "Heating",
        },
    },
    # Fan Speed (dp_id: 5)
    "fan_speed_enum": {
        "dp_id": 5,
        "code": "fan_speed_enum",
        "name": "Fan Speed",
        "icon": "mdi:fan",
        "options": {
            "0": "Off",
            "1": "Silent",
            "2": "Low",
            "3": "Medium-Low",
            "4": "Medium",
            "5": "Medium-High",
            "6": "High",
            "7": "Powerful",
        },
    },
    # Vertical Swing (dp_id: 31)
    "gear_vertical": {
        "dp_id": 31,
        "code": "gear_vertical",
        "name": "Vertical Swing",
        "icon": "mdi:arrow-up-down",
        "options": {
            "0": "Disabled",
            "1": "Swing",
            "2": "Up",
            "3": "Down",
            "4": "Reserved",
            "5": "Reserved",
            "6": "Encircle",
            "7": "Reserved",
            "8": "Stop Current",
            "9": "Stop Up",
            "10": "Stop Up-Mid",
            "11": "Stop Mid",
            "12": "Stop Down-Mid",
            "13": "Stop Down",
        },
    },
    # Horizontal Swing (dp_id: 34)
    "gear_horizontal": {
        "dp_id": 34,
        "code": "gear_horizontal",
        "name": "Horizontal Swing",
        "icon": "mdi:arrow-left-right",
        "options": {
            "0": "Disabled",
            "1": "Swing",
            "2": "Left",
            "3": "Mid",
            "4": "Right",
            "5": "Opposite",
            "6": "Reserved",
            "7": "Reserved",
            "8": "Stop Current",
            "9": "Stop Left",
            "10": "Stop Left-Mid",
            "11": "Stop Mid",
            "12": "Stop Right-Mid",
            "13": "Stop Right",
            "14": "Reserved",
            "15": "Reserved",
            "16": "Reserved",
            "17": "Encircle",
        },
    },
    # Fresh Air Fan Speed (dp_id: 40)
    "supply_fan_speed": {
        "dp_id": 40,
        "code": "supply_fan_speed",
        "name": "Fresh Air Fan Speed",
        "icon": "mdi:fan",
        "options": {
            "0": "Off",
            "1": "Low",
            "2": "Medium",
            "3": "Powerful",
        },
    },
    # Soft Wind (dp_id: 123)
    "soft_wind": {
        "dp_id": 123,
        "code": "soft_wind",
        "name": "Soft Wind",
        "icon": "mdi:weather-windy",
        "options": {
            "0": "Off",
            "1": "On",
            "2": "Mode 2",
            "3": "Mode 3",
            "4": "Mode 4",
        },
    },
    # AI ECO Status (dp_id: 124)
    "ai_eco_status": {
        "dp_id": 124,
        "code": "ai_eco_status",
        "name": "AI ECO Status",
        "icon": "mdi:leaf",
        "options": {
            "0": "Off",
            "1": "Frequency Mode",
            "2": "PID Mode",
        },
    },
    # Regular Reporting (dp_id: 125)
    "regular_reporting": {
        "dp_id": 125,
        "code": "regular_reporting",
        "name": "Regular Reporting",
        "icon": "mdi:update",
        "options": {
            "0": "On Change",
            "1": "1 Hour Interval",
            "2": "Cloud Request",
        },
    },
    # Sleep Mode (dp_id: 126)
    "sleep_enum": {
        "dp_id": 126,
        "code": "sleep_enum",
        "name": "Sleep Mode",
        "icon": "mdi:sleep",
        "options": {
            "0": "Off",
            "1": "Standard",
            "2": "Elderly",
            "3": "Child",
        },
    },
    # Generator Mode (dp_id: 132)
    "generator_mode": {
        "dp_id": 132,
        "code": "generator_mode",
        "name": "Generator Mode",
        "icon": "mdi:generator",
        "options": {
            "0": "Off",
            "1": "Level 1",
            "2": "Level 2",
            "3": "Level 3",
            "4": "Level 4",
            "5": "Level 5",
            "6": "Level 6",
        },
    },
    # Vertical Wind (dp_id: 137)
    "vertical_wind": {
        "dp_id": 137,
        "code": "vertical_wind",
        "name": "Vertical Wind",
        "icon": "mdi:arrow-up-down",
        "options": {
            "0": "Off",
            "1": "On",
        },
    },
    # Horizontal Wind (dp_id: 138)
    "horizontal_wind": {
        "dp_id": 138,
        "code": "horizontal_wind",
        "name": "Horizontal Wind",
        "icon": "mdi:arrow-left-right",
        "options": {
            "0": "Off",
            "1": "On",
        },
    },
    # Wakeup Word (dp_id: 139)
    "wakeup_word": {
        "dp_id": 139,
        "code": "wakeup_word",
        "name": "Wakeup Word Status",
        "icon": "mdi:microphone",
        "options": {
            "0": "No Custom",
            "1": "Custom Set",
            "2": "Clear Custom",
            "3": "Custom Used",
        },
    },
    # Wakeup Status (dp_id: 140)
    "wakeup_status": {
        "dp_id": 140,
        "code": "wakeup_status",
        "name": "Wakeup Learning Status",
        "icon": "mdi:microphone",
        "options": {
            "0": "Learning",
            "1": "First Success",
            "2": "Second Success",
            "3": "Third Success",
            "129": "First Failed",
            "130": "Second Failed",
        },
    },
    # Voice Status (dp_id: 143)
    "voice_status": {
        "dp_id": 143,
        "code": "voice_status",
        "name": "Voice Status",
        "icon": "mdi:microphone",
        "options": {
            "0": "Standby",
            "1": "Listening",
            "2": "Recognized",
            "3": "Command Failed",
            "4": "Playing",
            "5": "Content Playing",
        },
    },
    # Sound Location (dp_id: 146)
    "sound_location": {
        "dp_id": 146,
        "code": "sound_location",
        "name": "Sound Location",
        "icon": "mdi:map-marker",
        "options": {
            "0": "Location 0",
            "1": "Location 1",
            "2": "Location 2",
            "3": "Location 3",
            "4": "Location 4",
        },
    },
    # Smart Wind Mode (dp_id: 147)
    "smart_windmode": {
        "dp_id": 147,
        "code": "smart_windmode",
        "name": "Smart Wind Mode",
        "icon": "mdi:wind-turbine",
        "options": {
            "0": "Off",
            "1": "Avoid Person",
            "2": "Follow Person",
        },
    },
    # Auto Generator Mode (dp_id: 151)
    "auto_gen_mode": {
        "dp_id": 151,
        "code": "auto_gen_mode",
        "name": "Auto Generator Mode",
        "icon": "mdi:generator",
        "options": {
            "0": "Off",
            "1": "Level 1",
            "2": "Level 2",
            "3": "Level 3",
            "4": "Level 4",
            "5": "Level 5",
            "6": "Level 6",
            "7": "Turn Off",
        },
    },
    # Power Source (dp_id: 152)
    "power_source": {
        "dp_id": 152,
        "code": "power_source",
        "name": "Power Source",
        "icon": "mdi:power-plug",
        "options": {
            "0": "Grid",
            "1": "Generator",
        },
    },
    # BLE Module Status (dp_id: 153)
    "ble_module_status": {
        "dp_id": 153,
        "code": "ble_module_status",
        "name": "BLE Module Status",
        "icon": "mdi:bluetooth",
        "options": {
            "0": "Not Paired",
            "1": "Paired",
        },
    },
    # Left HT Direction (dp_id: 161)
    "left_ht_direction": {
        "dp_id": 161,
        "code": "left_ht_direction",
        "name": "Left HT Direction",
        "icon": "mdi:arrow-left",
        "options": {
            "0": "0",
            "1": "1",
            "2": "2",
            "3": "3",
            "4": "4",
            "5": "5",
            "6": "6",
            "7": "7",
            "8": "8",
            "9": "9",
            "10": "10",
            "11": "11",
            "12": "12",
            "13": "13",
            "14": "14",
            "15": "15",
            "16": "16",
            "17": "17",
            "18": "18",
        },
    },
    # Right HT Direction (dp_id: 162)
    "right_ht_direction": {
        "dp_id": 162,
        "code": "right_ht_direction",
        "name": "Right HT Direction",
        "icon": "mdi:arrow-right",
        "options": {
            "0": "0",
            "1": "1",
            "2": "2",
            "3": "3",
            "4": "4",
            "5": "5",
            "6": "6",
            "7": "7",
            "8": "8",
            "9": "9",
            "10": "10",
            "11": "11",
            "12": "12",
            "13": "13",
            "14": "14",
            "15": "15",
            "16": "16",
            "17": "17",
            "18": "18",
        },
    },
    # 3D Wind Type (dp_id: 164)
    "wind3d_type": {
        "dp_id": 164,
        "code": "wind3d_type",
        "name": "3D Wind Type",
        "icon": "mdi:fan",
        "options": {
            "0": "Type 0",
            "1": "Type 1",
        },
    },
    # Solar State (dp_id: 168)
    "solar_state": {
        "dp_id": 168,
        "code": "solar_state",
        "name": "Solar State",
        "icon": "mdi:solar-power",
        "options": {
            "0": "Off",
            "1": "On",
        },
    },
    # ADR Request (dp_id: 172)
    "openadr_request": {
        "dp_id": 172,
        "code": "openadr_request",
        "name": "ADR Request",
        "icon": "mdi:power-settings",
        "options": {
            "0": "No Request",
            "1": "Request",
        },
    },
}
