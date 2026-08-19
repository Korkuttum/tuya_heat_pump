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

"""Raw-field entries generated by raw_explorer.py
Device: bf6c66a96df4021d27z1nf
Generated: 2026-08-19 11:26:32

Paste this whole file at the BOTTOM of the device model file, as-is.
Each block below merges into the matching dict (SENSOR_TYPES,
SWITCH_TYPES, NUMBER_TYPES, SELECT_TYPES, TEXT_TYPES) via .update(),
so it adds to whatever is already defined earlier in the file —
it will NOT wipe out existing entries, even if that dict name is
already used for plain (non-raw) DPs elsewhere in the same file.
The integration reads `raw_source` + `field_index` to decode/encode
the value from a raw payload rather than a plain DP.
"""

# --- merge into SENSOR_TYPES (safe even if already defined above) ---
SENSOR_TYPES = globals().get("SENSOR_TYPES", {})
SENSOR_TYPES.update({
    "dhw_temp": {
        "dp_id": 119,
        "code": "dhw_temp",
        "raw_source": "pg60_status",
        "field_index": 0,
        "encoding": "int32_be",
        "name": "DHW temp",
        "unit": "°C",
        "icon": "mdi:thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
    },
    "btw_temp": {
        "dp_id": 119,
        "code": "btw_temp",
        "raw_source": "pg60_status",
        "field_index": 1,
        "encoding": "int32_be",
        "name": "BTW temp",
        "unit": "°C",
        "icon": "mdi:thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
    },
    "btw_inlet_temp": {
        "dp_id": 119,
        "code": "btw_inlet_temp",
        "raw_source": "pg60_status",
        "field_index": 2,
        "encoding": "int32_be",
        "name": "BTW inlet temp",
        "unit": "°C",
        "icon": "mdi:thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
    },
    "btw_outlet_temp": {
        "dp_id": 119,
        "code": "btw_outlet_temp",
        "raw_source": "pg60_status",
        "field_index": 3,
        "encoding": "int32_be",
        "name": "BTW outlet temp",
        "unit": "°C",
        "icon": "mdi:thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
    },
    "heating_coil_temp": {
        "dp_id": 119,
        "code": "heating_coil_temp",
        "raw_source": "pg60_status",
        "field_index": 4,
        "encoding": "int32_be",
        "name": "Heating coil temp",
        "unit": "°C",
        "icon": "mdi:thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
    },
    "cooling_coil_temp": {
        "dp_id": 119,
        "code": "cooling_coil_temp",
        "raw_source": "pg60_status",
        "field_index": 5,
        "encoding": "int32_be",
        "name": "Cooling coil temp",
        "unit": "°C",
        "icon": "mdi:thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
    },
    "exhaust_coil_temp": {
        "dp_id": 119,
        "code": "exhaust_coil_temp",
        "raw_source": "pg60_status",
        "field_index": 6,
        "encoding": "int32_be",
        "name": "Exhaust coil temp",
        "unit": "°C",
        "icon": "mdi:thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
    },
    "evap_temp": {
        "dp_id": 119,
        "code": "evap_temp",
        "raw_source": "pg60_status",
        "field_index": 7,
        "encoding": "int32_be",
        "name": "Evap temp",
        "unit": "°C",
        "icon": "mdi:thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
    },
    "ambient_temp": {
        "dp_id": 119,
        "code": "ambient_temp",
        "raw_source": "pg60_status",
        "field_index": 8,
        "encoding": "int32_be",
        "name": "Ambient temp",
        "unit": "°C",
        "icon": "mdi:thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
    },
    "expansion_valve": {
        "dp_id": 119,
        "code": "expansion_valve",
        "raw_source": "pg60_status",
        "field_index": 9,
        "encoding": "int32_be",
        "name": "Expansion valve",
        "unit": "step",
        "icon": "mdi:pipe-valve",
    },
    "evi_inlet_temp": {
        "dp_id": 119,
        "code": "evi_inlet_temp",
        "raw_source": "pg60_status",
        "field_index": 10,
        "encoding": "int32_be",
        "name": "EVI inlet temp",
        "unit": "°C",
        "icon": "mdi:thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
    },
    "solar_water_temp": {
        "dp_id": 119,
        "code": "solar_water_temp",
        "raw_source": "pg60_status",
        "field_index": 11,
        "encoding": "int32_be",
        "name": "Solar water temp",
        "unit": "°C",
        "icon": "mdi:thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
    },
    "ipm_temp": {
        "dp_id": 119,
        "code": "ipm_temp",
        "raw_source": "pg60_status",
        "field_index": 12,
        "encoding": "int32_be",
        "name": "IPM temp",
        "unit": "°C",
        "icon": "mdi:thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
    },
    "comp_freq": {
        "dp_id": 119,
        "code": "comp_freq",
        "raw_source": "pg60_status",
        "field_index": 13,
        "encoding": "int32_be",
        "name": "Comp freq",
        "unit": "Hz",
        "icon": "mdi:cosine-wave",
        "device_class": "frequency",
        "state_class": "measurement",
    },
    "comp_current": {
        "dp_id": 119,
        "code": "comp_current",
        "raw_source": "pg60_status",
        "field_index": 14,
        "encoding": "int32_be",
        "name": "Comp current",
        "unit": "A",
        "icon": "mdi:current-ac",
        "device_class": "current",
        "state_class": "measurement",
    },
    "comp_type": {
        "dp_id": 119,
        "code": "comp_type",
        "raw_source": "pg60_status",
        "field_index": 15,
        "encoding": "int32_be",
        "name": "Comp type",
    },
    "evi_outlet_temp": {
        "dp_id": 119,
        "code": "evi_outlet_temp",
        "raw_source": "pg60_status",
        "field_index": 16,
        "encoding": "int32_be",
        "name": "EVI outlet temp",
        "unit": "°C",
        "icon": "mdi:thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
    },
    "evi_valve": {
        "dp_id": 119,
        "code": "evi_valve",
        "raw_source": "pg60_status",
        "field_index": 17,
        "encoding": "int32_be",
        "name": "EVI valve",
        "unit": "step",
        "icon": "mdi:pipe-valve",
    },
    "dc_voltage": {
        "dp_id": 119,
        "code": "dc_voltage",
        "raw_source": "pg60_status",
        "field_index": 18,
        "encoding": "int32_be",
        "name": "DC voltage",
        "unit": "V",
        "icon": "mdi:lightning-bolt",
        "device_class": "voltage",
        "state_class": "measurement",
    },
    "fan_1_speed": {
        "dp_id": 119,
        "code": "fan_1_speed",
        "raw_source": "pg60_status",
        "field_index": 19,
        "encoding": "int32_be",
        "name": "Fan 1 speed",
        "unit": "rpm",
        "icon": "mdi:fan",
    },
    "fan_2_speed": {
        "dp_id": 119,
        "code": "fan_2_speed",
        "raw_source": "pg60_status",
        "field_index": 20,
        "encoding": "int32_be",
        "name": "Fan 2 speed",
        "unit": "rpm",
        "icon": "mdi:fan",
    },
    "l_pressure": {
        "dp_id": 119,
        "code": "l_pressure",
        "raw_source": "pg60_status",
        "field_index": 21,
        "encoding": "int32_be",
        "name": "L pressure",
        "unit": "bar",
    },
    "h_pressure": {
        "dp_id": 119,
        "code": "h_pressure",
        "raw_source": "pg60_status",
        "field_index": 22,
        "encoding": "int32_be",
        "name": "H pressure",
        "unit": "bar",
    },
    "l_temp": {
        "dp_id": 119,
        "code": "l_temp",
        "raw_source": "pg60_status",
        "field_index": 23,
        "encoding": "int32_be",
        "name": "L temp",
        "unit": "°C",
        "icon": "mdi:thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
    },
    "h_temp": {
        "dp_id": 119,
        "code": "h_temp",
        "raw_source": "pg60_status",
        "field_index": 24,
        "encoding": "int32_be",
        "name": "H temp",
        "unit": "°C",
        "icon": "mdi:thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
    },
    "ground_in_temp": {
        "dp_id": 119,
        "code": "ground_in_temp",
        "raw_source": "pg60_status",
        "field_index": 25,
        "encoding": "int32_be",
        "name": "Ground in temp",
        "unit": "°C",
        "icon": "mdi:thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
    },
    "ground_out_temp": {
        "dp_id": 119,
        "code": "ground_out_temp",
        "raw_source": "pg60_status",
        "field_index": 26,
        "encoding": "int32_be",
        "name": "Ground out temp",
        "unit": "°C",
        "icon": "mdi:thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
    },
    "pump_operation_hour": {
        "dp_id": 119,
        "code": "pump_operation_hour",
        "raw_source": "pg60_status",
        "field_index": 27,
        "encoding": "int32_be",
        "name": "Pump operation hour",
        "unit": "h",
    },
    "comp_operation_hour": {
        "dp_id": 119,
        "code": "comp_operation_hour",
        "raw_source": "pg60_status",
        "field_index": 28,
        "encoding": "int32_be",
        "name": "Comp operation hour",
        "unit": "h",
    },
    "btw_add1opertaion_hour": {
        "dp_id": 119,
        "code": "btw_add1opertaion_hour",
        "raw_source": "pg60_status",
        "field_index": 29,
        "encoding": "int32_be",
        "name": "BTW add1opertaion hour",
        "unit": "h",
    },
    "btw_add2opertaion_hour": {
        "dp_id": 119,
        "code": "btw_add2opertaion_hour",
        "raw_source": "pg60_status",
        "field_index": 30,
        "encoding": "int32_be",
        "name": "BTW add2opertaion hour",
        "unit": "h",
    },
    "dhw_add_operation_hour": {
        "dp_id": 119,
        "code": "dhw_add_operation_hour",
        "raw_source": "pg60_status",
        "field_index": 31,
        "encoding": "int32_be",
        "name": "DHW add operation hour",
        "unit": "h",
    },
    "pump_operation_time": {
        "dp_id": 119,
        "code": "pump_operation_time",
        "raw_source": "pg60_status",
        "field_index": 32,
        "encoding": "int32_be",
        "name": "Pump operation time",
        "unit": "m",
    },
    "comp_operation_time": {
        "dp_id": 119,
        "code": "comp_operation_time",
        "raw_source": "pg60_status",
        "field_index": 33,
        "encoding": "int32_be",
        "name": "Comp operation time",
        "unit": "m",
    },
    "btw_add1opertaion_time": {
        "dp_id": 119,
        "code": "btw_add1opertaion_time",
        "raw_source": "pg60_status",
        "field_index": 34,
        "encoding": "int32_be",
        "name": "BTW add1opertaion time",
        "unit": "m",
    },
    "btw_add2opertaion_time": {
        "dp_id": 119,
        "code": "btw_add2opertaion_time",
        "raw_source": "pg60_status",
        "field_index": 35,
        "encoding": "int32_be",
        "name": "BTW add2opertaion time",
        "unit": "m",
    },
    "dhw_add_operation_time": {
        "dp_id": 119,
        "code": "dhw_add_operation_time",
        "raw_source": "pg60_status",
        "field_index": 36,
        "encoding": "int32_be",
        "name": "DHW add operation time",
        "unit": "m",
    },
    "dxpump_operation_hour": {
        "dp_id": 119,
        "code": "dxpump_operation_hour",
        "raw_source": "pg60_status",
        "field_index": 37,
        "encoding": "int32_be",
        "name": "DXpump operation hour",
        "unit": "h",
    },
    "dxpump_operation_time": {
        "dp_id": 119,
        "code": "dxpump_operation_time",
        "raw_source": "pg60_status",
        "field_index": 38,
        "encoding": "int32_be",
        "name": "DXpump operation time",
        "unit": "A",
        "icon": "mdi:current-ac",
        "device_class": "current",
        "state_class": "measurement",
    },
    "ac_current": {
        "dp_id": 119,
        "code": "ac_current",
        "raw_source": "pg60_status",
        "field_index": 39,
        "encoding": "int32_be",
        "name": "AC current",
        "unit": "V",
        "icon": "mdi:lightning-bolt",
        "device_class": "voltage",
        "state_class": "measurement",
    },
    "ac_voltage": {
        "dp_id": 119,
        "code": "ac_voltage",
        "raw_source": "pg60_status",
        "field_index": 40,
        "encoding": "int32_be",
        "name": "AC voltage",
        "unit": "V",
        "icon": "mdi:lightning-bolt",
        "device_class": "voltage",
        "state_class": "measurement",
    },
    "power": {
        "dp_id": 119,
        "code": "power",
        "raw_source": "pg60_status",
        "field_index": 41,
        "encoding": "int32_be",
        "name": "Power",
        "unit": "W",
        "icon": "mdi:flash",
        "device_class": "power",
        "state_class": "measurement",
    },
    "heating_capacity": {
        "dp_id": 119,
        "code": "heating_capacity",
        "raw_source": "pg60_status",
        "field_index": 42,
        "encoding": "int32_be",
        "name": "Heating capacity",
        "unit": "W",
        "icon": "mdi:flash",
        "device_class": "power",
        "state_class": "measurement",
    },
    "cop": {
        "dp_id": 119,
        "code": "cop",
        "raw_source": "pg60_status",
        "field_index": 43,
        "encoding": "int32_be",
        "name": "COP",
    },
    "water_flow": {
        "dp_id": 119,
        "code": "water_flow",
        "raw_source": "pg60_status",
        "field_index": 44,
        "encoding": "int32_be",
        "name": "Water flow",
        "unit": "m3/h",
    },
    "heating_zone_2_temp": {
        "dp_id": 119,
        "code": "heating_zone_2_temp",
        "raw_source": "pg60_status",
        "field_index": 45,
        "encoding": "int32_be",
        "name": "Heating zone 2 temp",
        "unit": "°C",
        "icon": "mdi:thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
    },
    "heating_zone_3_temp": {
        "dp_id": 119,
        "code": "heating_zone_3_temp",
        "raw_source": "pg60_status",
        "field_index": 46,
        "encoding": "int32_be",
        "name": "Heating zone 3 temp",
        "unit": "°C",
        "icon": "mdi:thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
    },
    "heating_zone_2_valve": {
        "dp_id": 119,
        "code": "heating_zone_2_valve",
        "raw_source": "pg60_status",
        "field_index": 47,
        "encoding": "int32_be",
        "name": "Heating zone 2 valve",
    },
    "heating_zone_3_valve": {
        "dp_id": 119,
        "code": "heating_zone_3_valve",
        "raw_source": "pg60_status",
        "field_index": 48,
        "encoding": "int32_be",
        "name": "Heating zone 3 valve",
    },
    "antifreeze_temperature": {
        "dp_id": 119,
        "code": "antifreeze_temperature",
        "raw_source": "pg60_status",
        "field_index": 49,
        "encoding": "int32_be",
        "name": "Antifreeze temperature",
        "unit": "°C",
        "icon": "mdi:thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
    },
    "total_outlet_water_temperature": {
        "dp_id": 119,
        "code": "total_outlet_water_temperature",
        "raw_source": "pg60_status",
        "field_index": 50,
        "encoding": "int32_be",
        "name": "Total outlet water temperature",
        "unit": "°C",
        "icon": "mdi:thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
    },
    "main_ver": {
        "dp_id": 119,
        "code": "main_ver",
        "raw_source": "pg60_status",
        "field_index": 51,
        "encoding": "int32_be",
        "name": "Main Ver",
    },
})

# --- merge into SWITCH_TYPES (safe even if already defined above) ---
SWITCH_TYPES = globals().get("SWITCH_TYPES", {})
SWITCH_TYPES.update({
    "silent_mode": {
        "dp_id": 120,
        "code": "silent_mode",
        "raw_source": "pg60_group1",
        "field_index": 12,
        "encoding": "int32_be",
        "name": "Silent Mode",
        "icom": "mdi:volume-off",
    },
})

# --- merge into NUMBER_TYPES (safe even if already defined above) ---
NUMBER_TYPES = globals().get("NUMBER_TYPES", {})
NUMBER_TYPES.update({
    "dhw_set_t": {
        "dp_id": 120,
        "code": "dhw_set_t",
        "raw_source": "pg60_group1",
        "field_index": 0,
        "encoding": "int32_be",
        "min_value": 15,
        "max_value": 75,
        "step": 1,
        "name": "DHW Set T",
        "unit": "°C",
        "icon": "mdi:thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
    },
    "heat_set_t": {
        "dp_id": 120,
        "code": "heat_set_t",
        "raw_source": "pg60_group1",
        "field_index": 1,
        "encoding": "int32_be",
        "min_value": 10,
        "max_value": 60,
        "step": 1,
        "name": "Heat Set T",
        "unit": "°C",
        "icon": "mdi:thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
    },
    "cool_set_t": {
        "dp_id": 120,
        "code": "cool_set_t",
        "raw_source": "pg60_group1",
        "field_index": 2,
        "encoding": "int32_be",
        "min_value": 8,
        "max_value": 28,
        "step": 1,
        "name": "Cool Set T",
        "unit": "°C",
        "icon": "mdi:thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
    },
    "auto_set_t": {
        "dp_id": 120,
        "code": "auto_set_t",
        "raw_source": "pg60_group1",
        "field_index": 3,
        "encoding": "int32_be",
        "min_value": 15,
        "max_value": 25,
        "step": 1,
        "name": "AUTO Set T",
        "unit": "°C",
        "icon": "mdi:thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
    },
    "initial_btw_t": {
        "dp_id": 120,
        "code": "initial_btw_t",
        "raw_source": "pg60_group1",
        "field_index": 4,
        "encoding": "int32_be",
        "min_value": 15,
        "max_value": 25,
        "step": 1,
        "name": "Initial BTW T",
        "unit": "°C",
        "icon": "mdi:thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
    },
    "max_btw_t": {
        "dp_id": 120,
        "code": "max_btw_t",
        "raw_source": "pg60_group1",
        "field_index": 5,
        "encoding": "int32_be",
        "min_value": 24,
        "max_value": 55,
        "step": 1,
        "name": "Max BTW T",
        "unit": "°C",
        "icon": "mdi:thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
    },
    "dhw_δt": {
        "dp_id": 120,
        "code": "dhw_δt",
        "raw_source": "pg60_group1",
        "field_index": 6,
        "encoding": "int32_be",
        "min_value": 1,
        "max_value": 20,
        "step": 1,
        "name": "DHW ΔT",
        "unit": "°C",
        "icon": "mdi:thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
    },
    "btw_δt": {
        "dp_id": 120,
        "code": "btw_δt",
        "raw_source": "pg60_group1",
        "field_index": 7,
        "encoding": "int32_be",
        "min_value": 1,
        "max_value": 20,
        "step": 1,
        "name": "BTW ΔT",
        "unit": "°C",
        "icon": "mdi:thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
    },
    "silent_fre_set": {
        "dp_id": 120,
        "code": "silent_fre_set",
        "raw_source": "pg60_group1",
        "field_index": 8,
        "encoding": "int32_be",
        "min_value": 20,
        "max_value": 160,
        "step": 1,
        "name": "Silent Fre Set",
        "unit": "Hz",
        "icon": "mdi:cosine-wave",
        "device_class": "frequency",
        "state_class": "measurement",
    },
    "silent_fan_speed": {
        "dp_id": 120,
        "code": "silent_fan_speed",
        "raw_source": "pg60_group1",
        "field_index": 9,
        "encoding": "int32_be",
        "min_value": 30,
        "max_value": 90,
        "step": 1,
        "name": "Silent Fan Speed",
        "unit": "rpm",
        "icon": "mdi:fan",
    },
    "silent_start_time": {
        "dp_id": 120,
        "code": "silent_start_time",
        "raw_source": "pg60_group1",
        "field_index": 10,
        "encoding": "int32_be",
        "min_value": 0,
        "max_value": 23,
        "step": 1,
        "name": "Silent Start Time",
        "unit": "h",
    },
    "silent_stop_time": {
        "dp_id": 120,
        "code": "silent_stop_time",
        "raw_source": "pg60_group1",
        "field_index": 11,
        "encoding": "int32_be",
        "min_value": 0,
        "max_value": 23,
        "step": 1,
        "name": "Silent Stop Time",
        "unit": "h",
    },
})

