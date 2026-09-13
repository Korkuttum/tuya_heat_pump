"""Model mapping for Macon/Arctic Heat Pump (e1kt0dis)."""

MODEL_NAME = "Macon/Arctic Heat Pump (e1kt0dis)"
# ====================================================
# Macon/Arctic Heat Pump @superman22x
# ====================================================
# Plain DPs (switch/mode/fault/temp_unit_convert/setpoints/fre_mode/
# sample_fre_set) taken directly from this device's own typeSpec.
#
# UNRESOLVED — status_group_1 (dp 116) and status_group_2 (dp 117) are
# 80-byte raw blocks that almost certainly hold live telemetry (temps,
# pressures, etc.), but Tuya's model metadata gives no field-level
# breakdown, and there's no confirmed device-side correlation yet — run
# test/raw_explorer.py against the real device to map them.
#
# user_group_1-3, factory_group_1-6, tempset_group, timer_set_group and
# timer_en_group are raw config/schedule blocks, not live sensors —
# skipped.

SENSOR_TYPES = {
    "temp_current": {
        "dp_id": 3,
        "code": "temp_current",
        "name": "Current Temperature",
        "unit": "°C",
        "icon": "mdi:thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
    },
    "temp_current_f": {
        "dp_id": 26,
        "code": "temp_current_f",
        "name": "Hot Water Temperature (Hybrid Mode)",
        "unit": "°C",
        "icon": "mdi:water-thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
    },
    # Fault Description (dp_id: 9) — decodes Tuya's 30-label bitmap into
    # readable fault codes, listing every active fault if more than one
    # bit is set at once.
    "fault": {
        "dp_id": 9,
        "code": "fault",
        "name": "Fault Description",
        "icon": "mdi:alert-circle",
        "conversion": (
            "', '.join(n for b, n in [(1,'E28_1'),(2,'E19'),(4,'E18'),"
            "(8,'E28_2'),(16,'E27'),(32,'r13'),(64,'E01'),(128,'E09'),"
            "(256,'E05'),(512,'E22'),(1024,'FA'),(2048,'P19'),(4096,'r06'),"
            "(8192,'r10'),(16384,'r11'),(32768,'r01'),(65536,'P11'),"
            "(131072,'P02'),(262144,'P06'),(524288,'P27'),(1048576,'PC'),"
            "(2097152,'P30'),(4194304,'P01'),(8388608,'E20'),(16777216,'E33'),"
            "(33554432,'E34'),(67108864,'EB'),(134217728,'EC'),"
            "(268435456,'P15'),(536870912,'P16')"
            "] if value & b) or 'OK'"
        ),
    },
}

# ====================================================
# BINARY SENSOR TYPES (read-only bool/bitmap - accessMode: "ro")
# ====================================================
BINARY_SENSOR_TYPES = {
    "fault": {
        "dp_id": 9,
        "code": "fault",
        "name": "Fault Status",
        "device_class": "problem",
        "conversion": "value != 0",
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
}

# ====================================================
# NUMBER TYPES (read-write value - accessMode: "rw")
# ====================================================
NUMBER_TYPES = {
    "temp_set_1": {
        "dp_id": 101,
        "code": "temp_set_1",
        "name": "Temperature Setpoint",
        "icon": "mdi:thermostat",
        "unit": "°C",
        "min_value": 0.0,
        "max_value": 194.0,
        "step": 1.0,
        "api_conversion": "value",
    },
    "temp_set_wth": {
        "dp_id": 102,
        "code": "temp_set_wth",
        "name": "Hot Water Setpoint (Hybrid Mode)",
        "icon": "mdi:water-thermometer",
        "unit": "°C",
        "min_value": 0.0,
        "max_value": 194.0,
        "step": 1.0,
        "api_conversion": "value",
    },
}

# ====================================================
# SELECT TYPES (read-write enum - accessMode: "rw")
# ====================================================
SELECT_TYPES = {
    # Mode (dp_id: 4) - ACC=Cooling, GW=Floor Heating, ACH=Fan Coil
    # Heating, WTH=Hot Water, AUTO=Auto, WTH_GW=Hot Water + Floor
    # Heating, WTH_ACC=Hot Water + Cooling
    "mode": {
        "dp_id": 4,
        "code": "mode",
        "name": "Mode",
        "icon": "mdi:hvac",
        "options": {
            "ACC": "Cooling",
            "GW": "Floor Heating",
            "ACH": "Fan Coil Heating",
            "WTH": "Hot Water",
            "AUTO": "Auto",
            "WTH_GW": "Hot Water + Floor Heating",
            "WTH_ACC": "Hot Water + Cooling",
        },
    },
    # Temperature Unit (dp_id: 17) - c, f
    "temp_unit_convert": {
        "dp_id": 17,
        "code": "temp_unit_convert",
        "name": "Temperature Unit",
        "icon": "mdi:thermometer",
        "options": {
            "c": "Celsius",
            "f": "Fahrenheit",
        },
    },
    # Frequency Mode (dp_id: 131) - 0=Eco, 1=Silent, 2=Strong
    "fre_mode": {
        "dp_id": 131,
        "code": "fre_mode",
        "name": "Frequency Mode",
        "icon": "mdi:speedometer",
        "options": {
            "0": "Eco",
            "1": "Silent",
            "2": "Strong",
        },
    },
    # Sample Frequency (dp_id: 130) — Tuya's own description marks this
    # "not shown in the app"; it only controls how often the device
    # reports its state, not device behavior. Exposed for completeness.
    "sample_fre_set": {
        "dp_id": 130,
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
