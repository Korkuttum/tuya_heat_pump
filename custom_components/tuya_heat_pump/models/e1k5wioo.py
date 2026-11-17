# ====================================================
# Ultimate T-PRO 12K (indoor unit "ULTIMATE TPRO 12K IDU") @rotor3, issue #121
# Tuya modelId: e1k5wioo
# Split air conditioner (Tuya category kt) with heating and cooling.
# Temperatures are sent with scale 2 (2160 = 21.6 degrees C).
#
# Mapped from the reporter's data. Several functions of the cloud
# schema depend on what the unit really has (swing, fresh air, voice
# module, ...). They are listed here as well; if one of them does
# nothing on your unit, it is simply not supported by it.
#
# Not exposed on purpose:
#   - temp_set_f, lowheat_tempf (dp 24, 176): Fahrenheit twins.
#   - temperature_type (dp 101): display unit of the panel.
#   - weektimer1/2, specialtimer (dp 107, 109, 136): timers as text.
#   - capabilities (dp 133) and error_code (dp 134): raw data, not
#     decoded yet.
#   - Outdoor unit service values that can be written by the cloud
#     (dp 118, 121, 122), cloud-only counters (dp 128-131, 195-199),
#     voice module, solar and OpenADR data points (dp 139-172, 194).
# ====================================================
"""Model mapping for Ultimate T-PRO 12K (e1k5wioo)."""

MODEL_NAME = "Ultimate T-PRO 12K (e1k5wioo)"

# Sensor Types - read-only
SENSOR_TYPES = {
    "temp_current": {
        "dp_id": 3,
        "code": "temp_current",
        "name": "Room Temperature",
        "unit": "°C",
        "icon": "mdi:thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
        "conversion": "value / 100",
    },
    "ure": {
        # Tuya's own code for the outdoor temperature.
        "dp_id": 116,
        "code": "ure",
        "name": "Outdoor Temperature",
        "unit": "°C",
        "icon": "mdi:thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
        "conversion": "value / 100",
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
        "icon": "mdi:sine-wave",
        "state_class": "measurement",
    },
    "outdoor_comptar_freqrun": {
        "dp_id": 120,
        "code": "outdoor_comptar_freqrun",
        "name": "Compressor Target Frequency",
        "icon": "mdi:sine-wave",
        "state_class": "measurement",
    },
    "electricity": {
        "dp_id": 127,
        "code": "electricity",
        "name": "Energy",
        "unit": "kWh",
        "icon": "mdi:lightning-bolt",
        "device_class": "energy",
        "state_class": "total_increasing",
        "conversion": "value / 100",
    },
}

# Binary Sensor Types - read-only
BINARY_SENSOR_TYPES = {
    "heat_status": {
        "dp_id": 103,
        "code": "heat_status",
        "name": "Electric Heater Active",
        "device_class": "running",
    },
    "filter_block_status": {
        "dp_id": 110,
        "code": "filter_block_status",
        "name": "Filter Blocked",
        "device_class": "problem",
    },
    "freshair_status": {
        "dp_id": 108,
        "code": "freshair_status",
        "name": "Fresh Air Blocked",
        "device_class": "problem",
    },
}

# Switch Types
SWITCH_TYPES = {
    "switch": {
        "dp_id": 1,
        "code": "switch",
        "name": "Power",
        "icon": "mdi:power",
    },
    "auto": {
        "dp_id": 7,
        "code": "auto",
        "name": "Auto Fan Speed",
        "icon": "mdi:fan-auto",
    },
    "eco": {
        "dp_id": 8,
        "code": "eco",
        "name": "Eco",
        "icon": "mdi:leaf",
    },
    "drying": {
        "dp_id": 9,
        "code": "drying",
        "name": "Drying",
        "icon": "mdi:water-percent",
    },
    "heat": {
        "dp_id": 12,
        "code": "heat",
        "name": "Electric Heater",
        "icon": "mdi:radiator",
    },
    "light": {
        "dp_id": 13,
        "code": "light",
        "name": "Display Light",
        "icon": "mdi:lightbulb",
    },
    "beep": {
        "dp_id": 16,
        "code": "beep",
        "name": "Beep",
        "icon": "mdi:volume-high",
    },
    "health": {
        "dp_id": 26,
        "code": "health",
        "name": "Health Function",
        "icon": "mdi:shield-check",
    },
    "cleaning": {
        "dp_id": 27,
        "code": "cleaning",
        "name": "Evaporator Cleaning",
        "icon": "mdi:spray-bottle",
    },
    "eight_add_hot": {
        "dp_id": 102,
        "code": "eight_add_hot",
        "name": "8 °C Heating",
        "icon": "mdi:snowflake-melt",
    },
    "high_temperature_wind": {
        "dp_id": 104,
        "code": "high_temperature_wind",
        "name": "High Temperature Wind",
        "icon": "mdi:weather-windy",
    },
    "cool_feel_wind": {
        "dp_id": 105,
        "code": "cool_feel_wind",
        "name": "Cool Feel Wind",
        "icon": "mdi:weather-windy-variant",
    },
    "ai_eco_switch": {
        "dp_id": 111,
        "code": "ai_eco_switch",
        "name": "AI Eco",
        "icon": "mdi:brain",
    },
    "anti_directblow": {
        "dp_id": 157,
        "code": "anti_directblow",
        "name": "Anti Direct Blow",
        "icon": "mdi:air-filter",
    },
    "fireplace_sw": {
        "dp_id": 173,
        "code": "fireplace_sw",
        "name": "Fireplace Mode",
        "icon": "mdi:fireplace",
    },
    "lowheat_sw": {
        "dp_id": 174,
        "code": "lowheat_sw",
        "name": "8-15 °C Heating",
        "icon": "mdi:snowflake-melt",
    },
}

# Number Types
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
        "api_conversion": "int(value * 100)",
    },
    "lowheat_tempc": {
        "dp_id": 175,
        "code": "lowheat_tempc",
        "name": "8-15 °C Heating Temperature",
        "icon": "mdi:thermometer-low",
        "unit": "°C",
        "min_value": 8.0,
        "max_value": 15.0,
        "step": 1.0,
        "conversion": "value / 100",
        "api_conversion": "int(value * 100)",
    },
}

# Select Types
SELECT_TYPES = {
    "mode": {
        "dp_id": 4,
        "code": "mode",
        "name": "Operating Mode",
        "icon": "mdi:hvac",
        "options": {
            "0": "Auto",
            "1": "Cooling",
            "2": "Dry",
            "3": "Fan",
            "4": "Heating",
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
            "7": "Turbo",
        },
    },
    "gear_vertical": {
        "dp_id": 31,
        "code": "gear_vertical",
        "name": "Vertical Air Direction",
        "icon": "mdi:arrow-up-down",
        "options": {
            "1": "Swing Up-Down",
            "2": "Up",
            "3": "Down",
            "6": "Surround",
            "8": "Hold Current Position",
            "9": "Hold Top",
            "10": "Hold Upper",
            "11": "Hold Middle",
            "12": "Hold Lower",
            "13": "Hold Bottom",
        },
    },
    "gear_horizontal": {
        "dp_id": 34,
        "code": "gear_horizontal",
        "name": "Horizontal Air Direction",
        "icon": "mdi:arrow-left-right",
        "options": {
            "1": "Swing Left-Right",
            "2": "Left",
            "3": "Center",
            "4": "Right",
            "5": "Opposing",
            "8": "Hold Current Position",
            "9": "Hold Left",
            "10": "Hold Left of Center",
            "11": "Hold Center",
            "12": "Hold Right of Center",
            "13": "Hold Right",
            "17": "Surround",
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
            "3": "Child",
        },
    },
}
