# ====================================================
# Mitsubishi Heavy Industries TWMBS 2203 J-1 @mircolino, issue #122
# Tuya modelId: 000004d65i
# Domestic hot water heat pump (app name "DHW heat pump") with a
# heat pump, an electric heater and a fan mode.
#
# The fault status is a bitmap. The labels of its bits, in order:
#   P01 lower tank sensor, P02 upper tank sensor, P03 coil sensor,
#   P04 return gas sensor, P05 ambient sensor, P06 winter antifreeze
#   protection, E01 high pressure, E02 low pressure, E03 overheat,
#   PA compressor limit (ambient or tank temperature), E08 communication,
#   E6 anode alarm, EA9 MCU ROM, CS defrost / refrigerant recovery.
# The single bits are not decoded yet; the sensor below only tells
# whether any of them is set.
#
# The three AI values (dp 101-103) are read-only data of the unit's
# "AI" function and are shown as they are.
# ====================================================
"""Model mapping for Mitsubishi Heavy Industries TWMBS 2203 J-1 (000004d65i)."""

MODEL_NAME = "Mitsubishi Heavy Industries TWMBS 2203 J-1 (000004d65i)"

# Sensor Types - read-only
SENSOR_TYPES = {
    "temp_current": {
        "dp_id": 3,
        "code": "temp_current",
        "name": "Water Temperature",
        "unit": "°C",
        "icon": "mdi:thermometer-water",
        "device_class": "temperature",
        "state_class": "measurement",
    },
    "ai_start_time": {
        "dp_id": 102,
        "code": "ai_start_time",
        "name": "AI Start Hour",
        "icon": "mdi:clock-start",
    },
    "ai_temp_setting": {
        "dp_id": 103,
        "code": "ai_temp_setting",
        "name": "AI Set Temperature",
        "unit": "°C",
        "icon": "mdi:thermometer-auto",
        "device_class": "temperature",
    },
}

# Binary Sensor Types - read-only
BINARY_SENSOR_TYPES = {
    "fault": {
        # Bitmap, 0 = no fault. Individual bits are not decoded.
        "dp_id": 21,
        "code": "fault",
        "name": "Fault Status",
        "device_class": "problem",
        "conversion": "value != 0",
    },
    "ai_mark": {
        "dp_id": 101,
        "code": "ai_mark",
        "name": "AI Data Recorded",
        "icon": "mdi:check-circle-outline",
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
}

# Number Types
NUMBER_TYPES = {
    "temp_set": {
        "dp_id": 2,
        "code": "temp_set",
        "name": "Target Temperature",
        "icon": "mdi:thermometer",
        "unit": "°C",
        "min_value": 35.0,
        "max_value": 70.0,
        "step": 1.0,
        "api_conversion": "int(value)",
    },
}

# Select Types
SELECT_TYPES = {
    "mode": {
        "dp_id": 4,
        "code": "mode",
        "name": "Operating Mode",
        "icon": "mdi:water-boiler",
        "options": {
            "auto": "Auto",
            "eco": "ECO",
            "mix": "Mix",
            "electric": "Electric Heater",
            "air": "Fan",
        },
    },
}
