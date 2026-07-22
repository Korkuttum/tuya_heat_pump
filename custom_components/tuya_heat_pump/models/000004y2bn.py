"""Model mapping for Adlar Castra Domestic Heat Pump (000004y2bn)."""

MODEL_NAME = "Adlar Castra Domestic Heat Pump (000004y2bn)"
# ====================================================
# Adlar Castra Domestic @BP0313430
# ====================================================

SENSOR_TYPES = {
    # Current Temperature (dp_id: 3)
    "temp_current": {
        "dp_id": 3,
        "code": "temp_current",
        "name": "Current Temperature",
        "unit": "°C",
        "icon": "mdi:thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
    },
    # Fault Description (dp_id: 9) — bit order below matches Tuya's
    # actual typeSpec.label array exactly (NOT the order the fault
    # codes appear in the semicolon-separated description text, which
    # is different and would give a wrong mapping for bits 9-14).
    "fault": {
        "dp_id": 9,
        "code": "fault",
        "name": "Fault Description",
        "icon": "mdi:alert-circle",
        "conversion": (
            "', '.join(n for b, n in ["
            "(1,'P01 - Water Tank Lower Temp Sensor Fault'),"
            "(2,'P02 - Water Tank Upper Temp Sensor Fault'),"
            "(4,'P03 - Coil Temp Sensor Fault'),"
            "(8,'P04 - Suction Gas Temp Sensor Fault'),"
            "(16,'P05 - Ambient Temp Sensor Fault'),"
            "(32,'P06 - Winter Anti-Freeze Protection'),"
            "(64,'E01 - High Pressure Protection'),"
            "(128,'E02 - Low Pressure Protection'),"
            "(256,'E03 - Overheat Protection'),"
            "(512,'E08 - Communication Fault'),"
            "(1024,'EA8 - MCU RAM Fault'),"
            "(2048,'EA9 - MCU ROM Fault'),"
            "(4096,'P08 - Reserved'),"
            "(8192,'P09 - Reserved'),"
            "(16384,'P07 - Compressor Operating Limit Protection')"
            "] if value & b) or 'OK'"
        ),
    },
}

# ====================================================
# BINARY SENSOR TYPES (read-only bitmap - accessMode: "ro")
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
    "Power": {
        "dp_id": 1,
        "code": "Power",
        "name": "Power",
        "icon": "mdi:power",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']",
    },
}

# ====================================================
# NUMBER TYPES (read-write value - accessMode: "rw")
# ====================================================
NUMBER_TYPES = {
    "temp_set": {
        "dp_id": 2,
        "code": "temp_set",
        "name": "Target Temperature",
        "icon": "mdi:thermostat",
        "unit": "°C",
        "min_value": 10.0,
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
        "dp_id": 4,
        "code": "mode",
        "name": "Mode",
        "icon": "mdi:hvac",
        "options": {
            "heat": "Heating",
            "heatfan": "Heating + Fan",
        },
    },
}
