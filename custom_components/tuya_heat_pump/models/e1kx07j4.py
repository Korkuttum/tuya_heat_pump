"""Model mapping for Lunna LV LT1530 / Nordic LV LT1530 Heat Pump (e1kx07j4)."""

MODEL_NAME = "Lunna LV LT1530 / Nordic LV LT1530 Heat Pump (e1kx07j4)"
# ====================================================
# Lunna LV LT1530 @strandman
# ====================================================
# ====================================================
# Lunna LV LT1530 (Nordic LV LT1530) — reported by @strandman, issue #78.
# Built from a single cloud properties + model dump (no live device access),
# so every field below is only as good as Tuya's own schema text — there is
# no independent confirmation of ranges or fault meanings the way PR #76's
# e1kt1inc fault table was confirmed by provoking real faults. Treat units,
# min/max, and fault names as best-effort until an owner confirms them.
#
# UNRESOLVED — "Silent mode" (the feature actually requested in #78):
# there is no dedicated silent/quiet DP in this schema at all. The device
# exposes 5 raw, undocumented parameter blocks instead:
#   - pg60_status  (dp 119, ro) — status parameter group
#   - pg60_group1  (dp 120, rw) — user parameter group 1
#   - pg60_group2  (dp 121, rw) — user parameter group 2
#   - pg60_group3  (dp 122, rw) — user parameter group 3
#   - pg60_group4  (dp 123, rw) — user parameter group 4
# Tuya's model metadata gives no field-level breakdown for any of these
# (unlike e.g. 000004jong's parameter_group_1..4, which a real device owner
# decoded field-by-field with test/raw_explorer.py). Silent mode is most
# likely a bit/byte inside one of the rw groups. To find it: run
# test/raw_explorer.py against the real device, note the group values with
# Silent mode OFF, toggle it ON in the Smart Life app, and see which single
# field changes — raw_explorer.py highlights changed fields live and can
# export a ready-to-paste snippet once the field is identified.
# ====================================================
SENSOR_TYPES = {
    # Fault Description (dp_id: 15) — decodes Tuya's bitmap (typeSpec.label)
    # into readable fault names instead of the raw bitmap integer, listing
    # every active fault if more than one bit is set at once.
    "fault": {
        "dp_id": 15,
        "code": "fault",
        "name": "Fault Description",
        "icon": "mdi:alert-circle",
        "conversion": (
            "', '.join(n for b, n in ["
            "(1,'E00'),(2,'E01'),(4,'E02'),(8,'E06'),(16,'E04'),(32,'E05'),"
            "(64,'E07'),(128,'E08'),(256,'E09'),(512,'E10'),(1024,'E11'),"
            "(2048,'E12'),(4096,'E13'),(8192,'E14'),(16384,'E16'),(32768,'E18'),"
            "(65536,'E19'),(131072,'E20'),(262144,'E21'),(524288,'E22'),"
            "(1048576,'E23'),(2097152,'E31'),(4194304,'E33'),(8388608,'E34'),"
            "(16777216,'E35'),(33554432,'E27'),(67108864,'E25'),(134217728,'E24'),"
            "(268435456,'E37'),(536870912,'E38')"
            "] if value & b) or 'OK'"
        ),
    },
    # Extra Fault Description (dp_id: 199) — second, separate fault bitmap
    # ("额外故障组" / extra fault group), same decode approach as above.
    "extra_fault": {
        "dp_id": 199,
        "code": "extra_fault",
        "name": "Extra Fault Description",
        "icon": "mdi:alert-circle-outline",
        "conversion": (
            "', '.join(n for b, n in ["
            "(1,'E15'),(2,'E39'),(4,'E40'),(8,'E51'),(16,'E41'),(32,'E42'),"
            "(64,'E43'),(128,'E44'),(256,'E49'),(512,'E50'),(1024,'E30'),"
            "(2048,'E_25_1'),(4096,'E_25_2'),(8192,'E_25_3'),(16384,'E_25_4'),"
            "(32768,'E_25_5'),(65536,'E_25_6'),(131072,'E_25_7'),(262144,'E_25_8'),"
            "(524288,'E_25_9'),(1048576,'E_25_10'),(2097152,'E_25_11'),"
            "(4194304,'E_25_12'),(8388608,'E_25_13'),(16777216,'E_25_14'),"
            "(33554432,'E_25_15'),(67108864,'E_25_16'),(134217728,'E53'),"
            "(268435456,'E52'),(536870912,'E54')"
            "] if value & b) or 'OK'"
        ),
    },
    # ECO Timer Slot (dp_id: 105) — read-only; which of the 4 scheduled
    # ECO timer slots is currently selected/active ("null" = none).
    "eco_timer": {
        "dp_id": 105,
        "code": "eco_timer",
        "name": "ECO Timer Slot",
        "icon": "mdi:timer-outline",
    },
    # Heat Setpoint Upper Limit (dp_id: 115) — read-only; the device's own
    # current ceiling for heat_settemp (see NUMBER_TYPES below).
    "heat_settempup": {
        "dp_id": 115,
        "code": "heat_settempup",
        "name": "Heat Setpoint Upper Limit",
        "unit": "°C",
        "icon": "mdi:thermometer-chevron-up",
        "device_class": "temperature",
        "state_class": "measurement",
    },
    # Heat Setpoint Lower Limit (dp_id: 116) — read-only; the device's own
    # current floor for heat_settemp (see NUMBER_TYPES below).
    "heat_settemplow": {
        "dp_id": 116,
        "code": "heat_settemplow",
        "name": "Heat Setpoint Lower Limit",
        "unit": "°C",
        "icon": "mdi:thermometer-chevron-down",
        "device_class": "temperature",
        "state_class": "measurement",
    },
}

# ====================================================
# BINARY SENSOR TYPES (read-only bool/bitmap - accessMode: "ro")
# ====================================================
BINARY_SENSOR_TYPES = {
    # Quick true/false view of the same DP as the "fault" sensor above.
    "fault": {
        "dp_id": 15,
        "code": "fault",
        "name": "Fault Status",
        "device_class": "problem",
        "conversion": "value != 0",
    },
    # Quick true/false view of the same DP as "extra_fault" above.
    "extra_fault": {
        "dp_id": 199,
        "code": "extra_fault",
        "name": "Extra Fault Status",
        "device_class": "problem",
        "conversion": "value != 0",
    },
    # Multi-Unit Linked (dp_id: 104) — "0: no linked unit, 1: linked unit
    # present" per Tuya's own description (多联机状态).
    "units_state": {
        "dp_id": 104,
        "code": "units_state",
        "name": "Multi-Unit Linked",
        "icon": "mdi:link-variant",
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
}

# ====================================================
# NUMBER TYPES (read-write value - accessMode: "rw")
# ====================================================
NUMBER_TYPES = {
    # Heat Setpoint (dp_id: 102). Tuya's own typeSpec range for this DP
    # (-100001..100000) is a template placeholder, not a real limit — the
    # device reports its actual current bounds itself via heat_settempup /
    # heat_settemplow (dp 115/116, see SENSOR_TYPES). The values below
    # (10-25°C) are the bounds seen in the one sample dump available;
    # confirm against those two sensors (or the Smart Life app) and adjust
    # if a real installation allows a wider range.
    "heat_settemp": {
        "dp_id": 102,
        "code": "heat_settemp",
        "name": "Heat Setpoint",
        "unit": "°C",
        "icon": "mdi:thermostat",
        "min_value": 10.0,
        "max_value": 25.0,
        "step": 1.0,
        "conversion": "int(value)",
        "api_conversion": "int(value)",
    },
}

# ====================================================
# SELECT TYPES (read-write enum - accessMode: "rw")
# ====================================================
SELECT_TYPES = {
    # Mode (dp_id: 2)
    "mode": {
        "dp_id": 2,
        "code": "mode",
        "name": "Mode",
        "icon": "mdi:hvac",
        "options": {
            "water": "Hot Water",
            "heat": "Heat",
            "cold": "Cool",
            "wah": "Hot Water + Heat",
            "wac": "Hot Water + Cool",
            "p_cold": "Passive Cool",
        },
    },
    # ECO Mode (dp_id: 103)
    "eco_mode": {
        "dp_id": 103,
        "code": "eco_mode",
        "name": "ECO Mode",
        "icon": "mdi:leaf",
        "options": {
            "none": "Off",
            "eco_ord": "Normal Heating",
            "eco_curve": "Curve Heating",
            "eco_time": "Timed Heating",
            "eco_pcool": "Passive Cooling",
        },
    },
    # Sample Frequency (dp_id: 101) — Tuya's own description marks this
    # "not shown in the app"; it only controls how often the device reports
    # its state, not device behavior. Exposed for completeness.
    "sample_fre_set": {
        "dp_id": 101,
        "code": "sample_fre_set",
        "name": "Sample Frequency",
        "icon": "mdi:timer-sync-outline",
        "options": {
            "0": "30s",
            "1": "60s",
            "2": "120s",
            "3": "180s",
            "4": "300s",
        },
    },
}
