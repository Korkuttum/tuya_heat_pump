# ====================================================
# Mitsubishi Heavy Industries TWMBS 2203 J-1 @mircolino, issue #122
# Tuya modelId: 000004d65i
# Domestic hot water heat pump (app name "DHW heat pump") with a
# heat pump, an electric heater and a fan mode.
#
# The fault status (dp 21) is a bitmap of 14 bits, one binary sensor
# per bit (the cloud's own labels, in order): P01 lower tank sensor,
# P02 upper tank sensor, P03 coil sensor, P04 return gas sensor, P05
# ambient sensor, P06 winter antifreeze protection, E01 high pressure,
# E02 low pressure, E03 overheat, PA compressor operating limit
# (ambient or tank temperature), E08 communication, E6 anode alarm,
# EA9 MCU ROM fault, CS defrost / refrigerant recovery (a state, not
# a fault). "Fault Status" is on while any bit is set. None of the
# bits has been seen set on a real unit yet.
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
        # Bitmap, 0 = no fault; on while any of the bits below is set.
        "dp_id": 21,
        "code": "fault",
        "name": "Fault Status",
        "device_class": "problem",
        "conversion": "value != 0",
    },
    # One sensor per bit of the fault bitmap, in the order of the labels
    # of the cloud schema (bit 0 = P01 ... bit 13 = CS).
    "fault_p01": {
        "dp_id": 21,
        "code": "fault",
        "name": "P01 Tank Lower Sensor Fault",
        "device_class": "problem",
        "icon": "mdi:thermometer-alert",
        "conversion": "(int(value) & 1) != 0",
    },
    "fault_p02": {
        "dp_id": 21,
        "code": "fault",
        "name": "P02 Tank Upper Sensor Fault",
        "device_class": "problem",
        "icon": "mdi:thermometer-alert",
        "conversion": "(int(value) & 2) != 0",
    },
    "fault_p03": {
        "dp_id": 21,
        "code": "fault",
        "name": "P03 Coil Sensor Fault",
        "device_class": "problem",
        "icon": "mdi:thermometer-alert",
        "conversion": "(int(value) & 4) != 0",
    },
    "fault_p04": {
        "dp_id": 21,
        "code": "fault",
        "name": "P04 Return Gas Sensor Fault",
        "device_class": "problem",
        "icon": "mdi:thermometer-alert",
        "conversion": "(int(value) & 8) != 0",
    },
    "fault_p05": {
        "dp_id": 21,
        "code": "fault",
        "name": "P05 Ambient Sensor Fault",
        "device_class": "problem",
        "icon": "mdi:thermometer-alert",
        "conversion": "(int(value) & 16) != 0",
    },
    "fault_p06": {
        "dp_id": 21,
        "code": "fault",
        "name": "P06 Winter Antifreeze Protection",
        "device_class": "problem",
        "icon": "mdi:snowflake-alert",
        "conversion": "(int(value) & 32) != 0",
    },
    "fault_e01": {
        "dp_id": 21,
        "code": "fault",
        "name": "E01 High Pressure Protection",
        "device_class": "problem",
        "icon": "mdi:gauge-full",
        "conversion": "(int(value) & 64) != 0",
    },
    "fault_e02": {
        "dp_id": 21,
        "code": "fault",
        "name": "E02 Low Pressure Protection",
        "device_class": "problem",
        "icon": "mdi:gauge-empty",
        "conversion": "(int(value) & 128) != 0",
    },
    "fault_e03": {
        "dp_id": 21,
        "code": "fault",
        "name": "E03 Overheat Protection",
        "device_class": "problem",
        "icon": "mdi:fire-alert",
        "conversion": "(int(value) & 256) != 0",
    },
    "fault_pa": {
        "dp_id": 21,
        "code": "fault",
        "name": "PA Operating Limit Protection",
        "device_class": "problem",
        "icon": "mdi:alert-circle-outline",
        "conversion": "(int(value) & 512) != 0",
    },
    "fault_e08": {
        "dp_id": 21,
        "code": "fault",
        "name": "E08 Communication Fault",
        "device_class": "problem",
        "icon": "mdi:lan-disconnect",
        "conversion": "(int(value) & 1024) != 0",
    },
    "fault_e6": {
        "dp_id": 21,
        "code": "fault",
        "name": "E6 Anode Alarm",
        "device_class": "problem",
        "icon": "mdi:alert-outline",
        "conversion": "(int(value) & 2048) != 0",
    },
    "fault_ea9": {
        "dp_id": 21,
        "code": "fault",
        "name": "EA9 MCU ROM Fault",
        "device_class": "problem",
        "icon": "mdi:chip",
        "conversion": "(int(value) & 4096) != 0",
    },
    "fault_cs": {
        "dp_id": 21,
        "code": "fault",
        "name": "CS Defrost / Refrigerant Recovery",
        "icon": "mdi:snowflake-melt",
        "conversion": "(int(value) & 8192) != 0",
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

# ====================================================
# Optional thermostat card (Options > thermostat). The unit has no
# data point that tells whether it is heating right now, so the card
# shows "heating" while the unit is on. The operating modes are offered
# as presets of the card; the temperature range of the card follows the
# target temperature (35-70 degrees C).
# ====================================================
CLIMATE_HINTS = {
    "defaults": {
        "power": "switch",
        "current": "temp_current",
        "target": "temp_set",
    },
    "preset": {
        "code": "mode",
        "values": ["auto", "eco", "mix", "electric", "air"],
    },
}
