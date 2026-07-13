"""Model mapping for WOPOLTOP Heat Pump (enhs6o)."""

MODEL_NAME = "WOPOLTOP Heat Pump (enhs6o)"
# ====================================================
# Wopoltop @goofee76
# ====================================================
SENSOR_TYPES = {
    # Current Temperature (dp_id: 3)
    "temp_current": {
        "dp_id": 3,
        "code": "temp_current",
        "name": "Current Temperature",
        "unit": "°F",
        "icon": "mdi:thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
    },
    # Fault Description (dp_id: 6) — key MUST match the real Tuya code
    # ("fault"), not an invented name like "fault_code": coordinator.data
    # is keyed by Tuya's own property code, so a mismatched key here
    # means this entity would always read as unknown/unavailable, even
    # though the DP itself is reporting fine.
    #
    # The DP is a 23-bit fault bitmap (see typeSpec.label in the device
    # model) — this decodes it into a human-readable name (or a comma
    # -separated list if more than one bit is set) instead of showing
    # the raw bitmap integer.
    "fault": {
        "dp_id": 6,
        "code": "fault",
        "name": "Fault Description",
        "icon": "mdi:alert-circle",
        "conversion": (
            "', '.join(n for b, n in ["
            "(1,'Ambient Temp Sensor Fault'),(2,'Water Tank Temp Sensor Fault'),"
            "(4,'Outlet Water Temp Sensor Fault'),(8,'Inlet Water Temp Sensor Fault'),"
            "(16,'Inner Coil Temp Sensor Fault'),(32,'Discharge Temp Sensor Fault'),"
            "(64,'Outer Coil Temp Sensor Fault'),(128,'Return Gas Temp Sensor Fault'),"
            "(256,'Indoor Ambient Temp Sensor Fault'),(512,'Aux Valve Front Temp Sensor Fault'),"
            "(1024,'Aux Valve Rear Temp Sensor Fault'),(2048,'Post-Throttle Temp Sensor Fault'),"
            "(4096,'High Pressure Sensor Fault'),(8192,'Low Pressure Sensor Fault'),"
            "(16384,'Reserved Fault 1'),(32768,'Reserved Fault 2'),"
            "(65536,'Discharge Temp Too High'),(131072,'High Pressure Fault'),"
            "(262144,'Low Pressure Fault'),(524288,'Water Flow Fault'),"
            "(1048576,'Heating Outlet Temp Too High'),(2097152,'Cooling Outlet Temp Too Low'),"
            "(4194304,'Water Temp Difference Too Large')"
            "] if value & b) or 'OK'"
        ),
    },
}

# ====================================================
# BINARY SENSOR TYPES (read-only bitmap - accessMode: "ro")
# ====================================================
BINARY_SENSOR_TYPES = {
    # Fault Status - Quick view (dp_id: 6). Same dp_id/key "fault" as the
    # sensor above is fine — SENSOR_TYPES and BINARY_SENSOR_TYPES are
    # separate dicts loaded by separate platforms (sensor.py vs
    # binary_sensor.py), and Home Assistant's entity registry scopes
    # unique_id per-domain, so sensor.xxx_fault and binary_sensor.xxx_fault
    # coexist without conflict.
    "fault": {
        "dp_id": 6,
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
    "temp_set": {
        "dp_id": 2,
        "code": "temp_set",
        "name": "Target Temperature",
        "icon": "mdi:thermostat",
        "unit": "°F",
        "min_value": 46.0,
        "max_value": 104.0,
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
        "name": "Working Mode",
        "icon": "mdi:hvac",
        "options": {
            "hot": "Heating",
            "cold": "Cooling",
            "auto": "Auto",
            "eco": "ECO",
        },
    },
}
