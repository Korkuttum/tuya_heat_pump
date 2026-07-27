"""Model mapping for Alps Exclusive Heat Pump (du1wh4)."""

MODEL_NAME = "Alps Exclusive Heat Pump (du1wh4)"
# ====================================================
# Alps Exclusive @simonboerstra
#
# Raw fields (parameter_group_1 through parameter_group_8, and
# parameter_group_23 — all 128-byte "raw" type blobs, dp_id 118-126,
# 140) are SKIPPED for now, not decoded. If simonboerstra runs
# raw_explorer.py on these, we can add individual fields from them
# later.
#
# NOTE: this device has NO plain adjustable target-temperature DP
# (no "temp_set" or equivalent) anywhere in the Standard set — it's
# possible the setpoint lives inside one of the raw parameter_group
# blobs above, meaning until those are decoded there's no way to see
# or change the target temperature through this integration yet.
# ====================================================

SENSOR_TYPES = {
    # Fault Alarm (dp_id: 15) — bitmap, 30 possible faults. Tuya's own
    # catalog gave no descriptions (just bare Er-codes) — meanings
    # below provided by @simonboerstra from his unit's manual, and
    # independently confirmed against a real Er05 (High Pressure
    # Fault) occurrence on his own device.
    "fault": {
        "dp_id": 15,
        "code": "fault",
        "name": "Fault Alarm",
        "icon": "mdi:alert-circle",
        "conversion": (
            "', '.join(n for b, n in ["
            "(1,'Er03 - Water Flow Failure'),"
            "(2,'Er04 - Antifreeze Protection'),"
            "(4,'Er05 - High Pressure Fault'),"
            "(8,'Er06 - Low Pressure Fault'),"
            "(16,'Er09 - Communication Failure'),"
            "(32,'Er10 - Frequency Conversion Module Communication Failure'),"
            "(64,'Er12 - Exhaust Temperature Too High Protection'),"
            "(128,'Er14 - Water Tank Temperature Sensor Fault'),"
            "(256,'Er15 - Water Inlet Temperature Sensor Fault'),"
            "(512,'Er16 - Evaporator Coil Temperature Sensor Fault'),"
            "(1024,'Er18 - Exhaust Temperature Sensor Fault'),"
            "(2048,'Er20 - Frequency Conversion Module Abnormal Protection'),"
            "(4096,'Er21 - Ambient Temperature Sensor Fault'),"
            "(8192,'Er23 - Cooling Outlet Water Temperature Supercooling Protection'),"
            "(16384,'Er26 - Heat Sink Temperature Sensor Fault'),"
            "(32768,'Er27 - Outlet Water Temperature Sensor Fault'),"
            "(65536,'Er29 - Return Gas Temperature Sensor Fault'),"
            "(131072,'Er32 - Heating Outlet Water Temperature Too High Protection'),"
            "(262144,'Er33 - Coil Temperature Too High'),"
            "(524288,'Er34 - Frequency Conversion Module Temperature Too High'),"
            "(1048576,'Er42 - Cooling Coil Temperature Sensor Failure'),"
            "(2097152,'Er62 - Economizer Inlet Temperature Sensor Fault'),"
            "(4194304,'Er63 - Economizer Outlet Temperature Sensor Fault'),"
            "(8388608,'Er64 - DC Fan 1 Fault'),"
            "(16777216,'Er66 - DC Fan 2 Fault'),"
            "(33554432,'Er67 - Low Pressure Switch Failure'),"
            "(67108864,'Er68 - High Pressure Switch Failure'),"
            "(134217728,'Er69 - Low Pressure Protection'),"
            "(268435456,'Er70 - High Pressure Protection'),"
            "(536870912,'Er73 - Compressor Discharge Overcurrent Protection')"
            "] if value & b) or 'OK'"
        ),
    },
    "intemp": {
        "dp_id": 101,
        "code": "intemp",
        "name": "Water Inlet Temperature",
        "unit": "°C",
        "icon": "mdi:thermometer-water",
        "device_class": "temperature",
        "state_class": "measurement",
    },
    "outtemp": {
        "dp_id": 102,
        "code": "outtemp",
        "name": "Water Outlet Temperature",
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
        "name": "Discharge Temperature",
        "unit": "°C",
        "icon": "mdi:thermometer-alert",
        "device_class": "temperature",
        "state_class": "measurement",
    },
    "hqtemp": {
        "dp_id": 105,
        "code": "hqtemp",
        "name": "Return Gas Temperature",
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
        "icon": "mdi:thermometer-water",
        "device_class": "temperature",
        "state_class": "measurement",
    },
    "step_run": {
        "dp_id": 109,
        "code": "step_run",
        "name": "Main Valve Opening",
        "unit": "P",
        "icon": "mdi:valve",
    },
    "stepb_run": {
        "dp_id": 111,
        "code": "stepb_run",
        "name": "EVI Valve Opening",
        "unit": "P",
        "icon": "mdi:valve",
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
        "icon": "mdi:flash",
        "device_class": "voltage",
        "state_class": "measurement",
    },
    "cmp_act_frep": {
        "dp_id": 115,
        "code": "cmp_act_frep",
        "name": "Compressor Frequency",
        "unit": "Hz",
        "icon": "mdi:sine-wave",
        "state_class": "measurement",
    },
    "dc_fan_speed": {
        "dp_id": 116,
        "code": "dc_fan_speed",
        "name": "DC Fan 1 Speed",
        "unit": "rpm",
        "icon": "mdi:fan",
        "state_class": "measurement",
    },
    "dc_fan2_speed": {
        "dp_id": 117,
        "code": "dc_fan2_speed",
        "name": "DC Fan 2 Speed",
        "unit": "rpm",
        "icon": "mdi:fan",
        "state_class": "measurement",
    },
}

# ====================================================
# BINARY SENSOR TYPES (read-only bitmap - accessMode: "ro")
# ====================================================
BINARY_SENSOR_TYPES = {
    "fault": {
        "dp_id": 15,
        "code": "fault",
        "name": "Fault Status",
        "device_class": "problem",
        "conversion": "value != 0",
    },
}

# ====================================================
# SWITCH TYPES (read-write bool - accessMode: "rw"/"wr")
# ====================================================
SWITCH_TYPES = {
    "switch": {
        "dp_id": 1,
        "code": "switch",
        "name": "Power",
        "icon": "mdi:power",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']",
    },
    # accessMode is "wr" (not the usual "rw") in Tuya's own schema —
    # a write-triggered action, only takes effect while the unit is
    # powered off (per Tuya's own description text for this DP).
    "reset": {
        "dp_id": 125,
        "code": "reset",
        "name": "Factory Reset",
        "icon": "mdi:restore",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']",
    },
}

# ====================================================
# NUMBER TYPES (read-write value - accessMode: "rw")
# ====================================================
# None found — see the note at the top of this file about the target
# temperature setpoint possibly living inside an undecoded raw
# parameter_group blob.
NUMBER_TYPES = {
}

# ====================================================
# SELECT TYPES (read-write enum - accessMode: "rw")
# ====================================================
SELECT_TYPES = {
    "mode": {
        "dp_id": 2,
        "code": "mode",
        "name": "Operating Mode",
        "icon": "mdi:hvac",
        "options": {
            "smart": "Smart",
            "strong": "Strong",
            "mute": "Mute",
        },
    },
    "work_mode": {
        "dp_id": 5,
        "code": "work_mode",
        "name": "Working Mode",
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
        "icon": "mdi:temperature-celsius",
        "options": {
            "c": "Celsius",
            "f": "Fahrenheit",
        },
    },
}
