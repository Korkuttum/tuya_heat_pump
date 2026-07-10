"""Model mapping for Reclaim Eco R290 Heat Pump (modelId: e1n3nme8)."""

MODEL_NAME = "Reclaim Eco R290 Heat Pump (e1n3nme8)"
# ====================================================
# Reclaim Eco R290 Heat Pump @peterkh
# modelId: e1n3nme8
# Notes:
#   - Domestic hot water (DHW) focused heat pump. Modes: water (normal),
#     boost, holiday, rescue.
#   - All temperature DPs use scale=0 (direct °C values).
#   - xd_cs / xd_tm / heat_tm are counters (units unknown, likely
#     minutes or cycle counts). Kept as raw sensors so the user can
#     observe and figure out over time.
#   - ds_switch (dp 101) purpose unknown, kept as a switch since it's
#     rw bool.
# ====================================================

SENSOR_TYPES = {
    # ---- Temperatures ----
    "temp_current": {
        "dp_id": 3,
        "code": "temp_current",
        "name": "Current Temperature",
        "unit": "°C",
        "icon": "mdi:thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
    },
    "tank": {
        "dp_id": 107,
        "code": "tank",
        "name": "Tank Temperature",
        "unit": "°C",
        "icon": "mdi:water-thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
    },
    "ambient": {
        "dp_id": 108,
        "code": "ambient",
        "name": "Ambient Temperature",
        "unit": "°C",
        "icon": "mdi:home-thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
    },
    "discharge": {
        "dp_id": 109,
        "code": "discharge",
        "name": "Discharge Temperature",
        "unit": "°C",
        "icon": "mdi:thermometer-alert",
        "device_class": "temperature",
        "state_class": "measurement",
    },
    "coil": {
        "dp_id": 110,
        "code": "coil",
        "name": "Coil Temperature",
        "unit": "°C",
        "icon": "mdi:thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
    },
    "suction": {
        "dp_id": 111,
        "code": "suction",
        "name": "Suction Temperature",
        "unit": "°C",
        "icon": "mdi:thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
    },

    # ---- Device state ----
    "eev_position": {
        "dp_id": 106,
        "code": "eev_position",
        "name": "EEV Position",
        "unit": "P",
        "icon": "mdi:pipe-valve",
        "state_class": "measurement",
    },
    "remaining_holiday": {
        "dp_id": 102,
        "code": "remaining_holiday",
        "name": "Remaining Holiday Days",
        "unit": "days",
        "icon": "mdi:calendar-clock",
        "state_class": "measurement",
    },
    "xd_cs": {
        "dp_id": 113,
        "code": "xd_cs",
        "name": "Defrost Cycles",
        "icon": "mdi:counter",
        "state_class": "measurement",
    },
    "xd_tm": {
        "dp_id": 114,
        "code": "xd_tm",
        "name": "Defrost Time",
        "icon": "mdi:timer",
        "state_class": "measurement",
    },
    "heat_tm": {
        "dp_id": 115,
        "code": "heat_tm",
        "name": "Heating Time",
        "icon": "mdi:timer",
        "state_class": "measurement",
    },
}

# ====================================================
# BINARY SENSOR TYPES
# ====================================================
BINARY_SENSOR_TYPES = {
    "fault": {
        "dp_id": 9,
        "code": "fault",
        "name": "Fault Alarm",
        "device_class": "problem",
        "conversion": "value != 0",
    },
    "compressor": {
        "dp_id": 103,
        "code": "compressor",
        "name": "Compressor",
        "device_class": "running",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']",
    },
    "fan": {
        "dp_id": 104,
        "code": "fan",
        "name": "Fan",
        "device_class": "running",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']",
    },
    "heating_element": {
        "dp_id": 105,
        "code": "heating_element",
        "name": "Backup Heater",
        "device_class": "heat",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']",
    },
    "defrost_valve": {
        "dp_id": 112,
        "code": "defrost_valve",
        "name": "Defrost Valve",
        "device_class": "opening",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']",
    },
}

# ====================================================
# SWITCH TYPES
# ====================================================
SWITCH_TYPES = {
    "Power": {
        "dp_id": 1,
        "code": "Power",
        "name": "Power",
        "icon": "mdi:power",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']",
    },
    "ds_switch": {
        "dp_id": 101,
        "code": "ds_switch",
        "name": "DS Switch",
        "icon": "mdi:toggle-switch",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']",
    },
    "disinfect": {
        "dp_id": 116,
        "code": "disinfect",
        "name": "Disinfection Mode",
        "icon": "mdi:shield-check",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']",
    },
}

# ====================================================
# NUMBER TYPES
# ====================================================
NUMBER_TYPES = {
    "temp_set": {
        "dp_id": 2,
        "code": "temp_set",
        "name": "Temperature Setpoint",
        "icon": "mdi:thermostat",
        "unit": "°C",
        "min_value": 10.0,
        "max_value": 65.0,
        "step": 1.0,
        "api_conversion": "int(value)",
    },
}

# ====================================================
# SELECT TYPES
# ====================================================
SELECT_TYPES = {
    "mode": {
        "dp_id": 4,
        "code": "mode",
        "name": "Operation Mode",
        "icon": "mdi:hvac",
        "options": {
            "water": "Normal",
            "boost": "Boost",
            "holiday": "Holiday",
            "rescue": "Rescue",
        },
    },
}
