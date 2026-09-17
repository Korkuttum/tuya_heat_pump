"""Model mapping for Rinnai Enviroflo GR / EHPG280VM Heat Pump (fxv5bw)."""

MODEL_NAME = "Rinnai Enviroflo GR / EHPG280VM Heat Pump (fxv5bw)"
# ====================================================
# Rinnai Enviroflo GR Series (EHPG280VM) @greengumbyaus
# ====================================================
# Every DP already carries a clean English name in Tuya's own schema —
# no raw payloads or translation guesswork needed here. temp_current
# (dp 3) and tank_temp (dp 103) read the same physical sensor (matching
# live values in the sample dump) — both kept since dp 103 is part of
# the diagnostic sensor group. timer (dp 15, 128-byte raw) is a
# schedule/config blob, not live telemetry — skipped.

SENSOR_TYPES = {
    "temp_current": {
        "dp_id": 3,
        "code": "temp_current",
        "name": "Water Tank Temperature",
        "unit": "°C",
        "icon": "mdi:water-thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
    },
    # Work State (dp_id: 8) — read-only status, not user-selectable.
    "work_state": {
        "dp_id": 8,
        "code": "work_state",
        "name": "Work State",
        "icon": "mdi:state-machine",
        "conversion": (
            "{'standby':'Standby','heating':'Heating','warm':'Keeping Warm'}"
            ".get(value, value)"
        ),
    },
    "ambient_temp": {
        "dp_id": 101,
        "code": "ambient_temp",
        "name": "Ambient Temperature",
        "unit": "°C",
        "icon": "mdi:home-thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
    },
    "discharge_temp": {
        "dp_id": 102,
        "code": "discharge_temp",
        "name": "Discharge Temperature",
        "unit": "°C",
        "icon": "mdi:thermometer-alert",
        "device_class": "temperature",
        "state_class": "measurement",
    },
    "tank_temp": {
        "dp_id": 103,
        "code": "tank_temp",
        "name": "Tank Temperature",
        "unit": "°C",
        "icon": "mdi:water-thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
    },
    "evaporator_temp": {
        "dp_id": 104,
        "code": "evaporator_temp",
        "name": "Evaporator Temperature",
        "unit": "°C",
        "icon": "mdi:thermometer-lines",
        "device_class": "temperature",
        "state_class": "measurement",
    },
    "suction_semp": {
        "dp_id": 105,
        "code": "suction_semp",
        "name": "Suction Temperature",
        "unit": "°C",
        "icon": "mdi:thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
    },
    "eev": {
        "dp_id": 107,
        "code": "eev",
        "name": "Expansion Valve Opening",
        "icon": "mdi:pipe-valve",
        "state_class": "measurement",
    },
    "mains_voltage": {
        "dp_id": 114,
        "code": "mains_voltage",
        "name": "Mains Voltage",
        "unit": "V",
        "icon": "mdi:lightning-bolt",
        "device_class": "voltage",
        "state_class": "measurement",
    },
    # Compressor Operation Time (dp_id: 118) — "this session's compressor
    # runtime" per Tuya's own (untranslated) name; no unit given in the
    # schema, so left unitless until confirmed.
    "comp_operation": {
        "dp_id": 118,
        "code": "comp_operation",
        "name": "Compressor Operation Time",
        "icon": "mdi:timer-outline",
        "state_class": "measurement",
    },
    # Unit On Duration (dp_id: 119) — "unit continuous working duration"
    # per Tuya's own (untranslated) name; no unit given in the schema,
    # so left unitless until confirmed.
    "unit_on": {
        "dp_id": 119,
        "code": "unit_on",
        "name": "Unit On Duration",
        "icon": "mdi:timer-outline",
        "state_class": "measurement",
    },
    "software_version": {
        "dp_id": 120,
        "code": "software_version",
        "name": "Software Version",
        "icon": "mdi:chip",
    },
    # Fault Description (dp_id: 18) — decodes Tuya's 12-label bitmap
    # into readable fault names, listing every active fault if more
    # than one bit is set at once.
    "fault": {
        "dp_id": 18,
        "code": "fault",
        "name": "Fault Description",
        "icon": "mdi:alert-circle",
        "conversion": (
            "', '.join(n for b, n in ["
            "(1,'E01: Ambient Temp Sensor Fault'),"
            "(2,'E02: Upper Tank Temp Sensor Fault'),"
            "(4,'E03: Discharge Temp Sensor Fault'),"
            "(8,'E04: Evaporator Temp Sensor Fault'),"
            "(16,'E05: Suction Temp Sensor Fault'),"
            "(32,'E06: Lower Tank Temp Sensor Fault'),"
            "(64,'E07: High Pressure Protection'),"
            "(128,'E08: Discharge Temp Too High'),"
            "(256,'E09: Low Voltage Protection'),"
            "(512,'E10: High Voltage Protection'),"
            "(1024,'E11: Fan Fault'),"
            "(2048,'E12: Anti-Freeze Protection')"
            "] if value & b) or 'OK'"
        ),
    },
}

# ====================================================
# BINARY SENSOR TYPES (read-only bool/bitmap - accessMode: "ro")
# ====================================================
BINARY_SENSOR_TYPES = {
    "fault": {
        "dp_id": 18,
        "code": "fault",
        "name": "Fault Status",
        "device_class": "problem",
        "conversion": "value != 0",
    },
    "high_pressure_switch": {
        "dp_id": 106,
        "code": "high_pressure_switch",
        "name": "High Pressure Switch",
        "icon": "mdi:gauge",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']",
    },
    "fan": {
        "dp_id": 108,
        "code": "fan",
        "name": "Fan Running",
        "device_class": "running",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']",
    },
    "compressor": {
        "dp_id": 109,
        "code": "compressor",
        "name": "Compressor Running",
        "device_class": "running",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']",
    },
    "way4": {
        "dp_id": 110,
        "code": "way4",
        "name": "Four-Way Valve Active",
        "icon": "mdi:valve",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']",
    },
    "defrost1": {
        "dp_id": 111,
        "code": "defrost1",
        "name": "Defrost Active",
        "device_class": "cold",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']",
    },
    "electrical_element": {
        "dp_id": 112,
        "code": "electrical_element",
        "name": "Electrical Heating Element Active",
        "device_class": "heat",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']",
    },
    "disinfection1": {
        "dp_id": 113,
        "code": "disinfection1",
        "name": "Disinfection Active",
        "icon": "mdi:water-boiler",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']",
    },
    "pv_signal": {
        "dp_id": 115,
        "code": "pv_signal",
        "name": "PV Signal",
        "icon": "mdi:solar-power",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']",
    },
    "off_peak": {
        "dp_id": 116,
        "code": "off_peak",
        "name": "Off-Peak Tariff Active",
        "icon": "mdi:clock-outline",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']",
    },
    "one_shot": {
        "dp_id": 117,
        "code": "one_shot",
        "name": "One-Shot Boost Active",
        "icon": "mdi:rocket-launch",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']",
    },
}

# ====================================================
# SWITCH TYPES (read-write bool - accessMode: "rw")
# ====================================================
SWITCH_TYPES = {
    "switch": {
        "dp_id": 1,
        "code": "switch",
        "name": "Power",
        "icon": "mdi:power",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']",
    },
    "child_lock": {
        "dp_id": 12,
        "code": "child_lock",
        "name": "Child Lock",
        "icon": "mdi:lock",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']",
    },
}

# ====================================================
# NUMBER TYPES (read-write value - accessMode: "rw")
# ====================================================
NUMBER_TYPES = {
    "temp_set": {
        "dp_id": 5,
        "code": "temp_set",
        "name": "Target Temperature",
        "icon": "mdi:thermostat",
        "unit": "°C",
        "min_value": 15.0,
        "max_value": 70.0,
        "step": 1.0,
        "api_conversion": "value",
    },
}

# ====================================================
# SELECT TYPES (read-write enum - accessMode: "rw")
# ====================================================
SELECT_TYPES = {
    "mode": {
        "dp_id": 2,
        "code": "mode",
        "name": "Mode",
        "icon": "mdi:hvac",
        "options": {
            "STANDARD": "Standard",
            "ECO": "Eco",
            "HYBRID": "Hybrid",
            "ELECTRIC": "Electric",
            "VACATION": "Vacation",
        },
    },
}
