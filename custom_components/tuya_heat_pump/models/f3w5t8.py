"""Model mapping for Alps Exclusive Heat Pump (f3w5t8)."""

MODEL_NAME = "Alps Exclusive Heat Pump (f3w5t8)"
# ====================================================
# Alps Exclusive (f3w5t8 variant) @jorisijji, issue #70
# ====================================================
# This is a DIFFERENT Tuya modelId from the Alps Exclusive already
# supported (du1wh4) — same brand, different internal hardware batch.
# With no model file of its own it was falling back to default.py,
# whose DP codes don't match this device at all, hence most entities
# showing unavailable.
#
# DP layout (switch/mode/work_mode/temp_unit_convert/wth_set/
# heating_set/cooling_set/status_parameter_group_1-2/
# parameter_group_1-10/reset/hdef/parameter_group_23/products_id/
# fault2/custom_fault_bit) is identical to the "Power World OEM" family
# (e1k5wjuc, e1nde5gc) — same dp_ids, same codes — so the plain DPs
# below are taken directly from this device's own typeSpec, matching
# that family's proven entity design.
#
# UNRESOLVED — raw parameter groups: status_parameter_group_1/2 (dp
# 101/102, likely live telemetry), parameter_group_1-10 (dp 118-124,
# 126-128, config) and parameter_group_23 (dp 140, "electricity
# statistics") have no field-level breakdown for this specific device —
# run test/raw_explorer.py to map them (same process as issue #53).
#
# fault (dp 15): 25 of this device's 30 codes match @simonboerstra's
# confirmed Alps translations (du1wh4, this same issue) one-for-one, so
# those are reused directly. The remaining 5 (Er72, Er74, Er75, Er76,
# Er01) don't appear in that list — shown as bare codes until someone
# provides their meaning.
#
# wth_set/heating_set/cooling_set: @tomoo777 found (issue #53, same OEM
# family) that e1k5wjuc silently multiplies whatever raw value it's
# written by 10 to get its real target temperature. This device's
# typeSpec is otherwise identical, so the same quirk is plausible here
# too — but NOT yet confirmed for this specific device, so left
# unscaled (api_conversion "value") rather than guessed. To check:
# type a value into one of these in HA, then look at the same setpoint
# in the Smart Life app — if the app shows 10× what you typed, apply
# the same "value / 10" fix used in e1k5wjuc.py.

SENSOR_TYPES = {
    # Fault Description (dp_id: 15) — see header note on translation
    # coverage.
    "fault": {
        "dp_id": 15,
        "code": "fault",
        "name": "Fault Description",
        "icon": "mdi:alert-circle",
        "conversion": (
            "', '.join(n for b, n in ["
            "(1,'Er03: Water flow failure'),"
            "(2,'Er73: Compressor discharge overcurrent protection'),"
            "(4,'Er05: High pressure fault'),"
            "(8,'Er06: Low pressure fault'),"
            "(16,'Er09: Communication failure'),"
            "(32,'Er10: Frequency conversion module communication failure'),"
            "(64,'Er12: Exhaust temperature too high protection'),"
            "(128,'Er14: Water tank temperature sensor fault'),"
            "(256,'Er15: Water inlet temperature sensor fault'),"
            "(512,'Er16: Evaporator coil temperature sensor fault'),"
            "(1024,'Er18: Exhaust temperature sensor fault'),"
            "(2048,'Er20: Frequency conversion module abnormal protection'),"
            "(4096,'Er21: Ambient temperature sensor fault'),"
            "(8192,'Er23: Cooling outlet water temperature supercooling protection'),"
            "(16384,'Er72'),"
            "(32768,'Er27: Outlet water temperature sensor fault'),"
            "(65536,'Er29: Return gas temperature sensor fault'),"
            "(131072,'Er32: Heating outlet water temperature too high protection'),"
            "(262144,'Er33: Coil temperature too high'),"
            "(524288,'Er74'),"
            "(1048576,'Er42: Cooling coil temperature sensor failure'),"
            "(2097152,'Er75'),"
            "(4194304,'Er76'),"
            "(8388608,'Er64: DC Fan 1 fault'),"
            "(16777216,'Er66: DC Fan 2 fault'),"
            "(33554432,'Er67: Low pressure switch failure'),"
            "(67108864,'Er68: High pressure switch failure'),"
            "(134217728,'Er69: Low pressure protection'),"
            "(268435456,'Er70: High pressure protection'),"
            "(536870912,'Er01')"
            "] if value & b) or 'OK'"
        ),
    },
    # Extra Fault Description (dp_id: 198) — DC water pump fault group.
    "fault2": {
        "dp_id": 198,
        "code": "fault2",
        "name": "Extra Fault Description",
        "icon": "mdi:alert-circle-outline",
        "conversion": (
            "', '.join(n for b, n in ["
            "(1,'Er79: DC Water Pump Undervoltage Fault'),"
            "(2,'Er80: DC Water Pump Stall/Locked-Rotor Fault'),"
            "(4,'Er81: DC Water Pump Other Fault'),"
            "(8,'Er82: DC Water Pump Communication Fault')"
            "] if value & b) or 'OK'"
        ),
    },
    # Custom Fault Bit (dp_id: 199) — inverter drive Er20 fault register,
    # per Tuya's own (untranslated) name for this DP.
    "custom_fault_bit": {
        "dp_id": 199,
        "code": "custom_fault_bit",
        "name": "Inverter Drive Fault Code",
        "icon": "mdi:alert-circle",
    },
    # Product ID (dp_id: 180)
    "products_id": {
        "dp_id": 180,
        "code": "products_id",
        "name": "Product ID",
        "icon": "mdi:identifier",
    },
}

# ====================================================
# BINARY SENSOR TYPES (read-only bool/bitmap - accessMode: "ro")
# ====================================================
BINARY_SENSOR_TYPES = {
    "fault": {
        "dp_id": 15,
        "code": "fault",
        "name": "Fault Status",
        "device_class": "problem",
        "conversion": "value != 0",
    },
    "fault2": {
        "dp_id": 198,
        "code": "fault2",
        "name": "Extra Fault Status",
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
    # Reset to Default (dp_id: 125) - accessMode: "wr"; Tuya's own
    # description notes this only takes effect while the unit is off.
    "reset": {
        "dp_id": 125,
        "code": "reset",
        "name": "Reset to Default",
        "icon": "mdi:restore",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']",
    },
}

# ====================================================
# NUMBER TYPES (read-write value - accessMode: "rw"/"wr")
# ====================================================
NUMBER_TYPES = {
    # See header note — write scaling unconfirmed for this device.
    "wth_set": {
        "dp_id": 110,
        "code": "wth_set",
        "name": "Hot Water Temperature",
        "icon": "mdi:water-thermometer",
        "unit": "°C",
        "min_value": 0.0,
        "max_value": 99.0,
        "step": 1.0,
        "api_conversion": "value",
    },
    "heating_set": {
        "dp_id": 111,
        "code": "heating_set",
        "name": "Heating Temperature",
        "icon": "mdi:thermostat",
        "unit": "°C",
        "min_value": 0.0,
        "max_value": 99.0,
        "step": 1.0,
        "api_conversion": "value",
    },
    "cooling_set": {
        "dp_id": 112,
        "code": "cooling_set",
        "name": "Cooling Temperature",
        "icon": "mdi:snowflake",
        "unit": "°C",
        "min_value": 0.0,
        "max_value": 99.0,
        "step": 1.0,
        "api_conversion": "value",
    },
    # Manual Defrost (dp_id: 130) - accessMode: "wr"
    "hdef": {
        "dp_id": 130,
        "code": "hdef",
        "name": "Manual Defrost",
        "icon": "mdi:snowflake-melt",
        "unit": "",
        "min_value": 1.0,
        "max_value": 8.0,
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
        "name": "Operation Mode",
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
        "name": "Work Mode",
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
        "icon": "mdi:thermometer",
        "options": {
            "c": "Celsius",
            "f": "Fahrenheit",
        },
    },
}
