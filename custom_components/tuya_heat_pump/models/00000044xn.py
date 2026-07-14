"""Model mapping for Poolex Dreamline Heat Pump (00000044xn)."""

MODEL_NAME = "Poolex Dreamline Heat Pump (00000044xn)"
# ====================================================
# Poolex @NicolasPasquelin
# ====================================================

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
    "ambient_temp": {
        "dp_id": 102,
        "code": "AmbientTemp",
        "name": "Ambient Temperature",
        "unit": "°C",
        "icon": "mdi:home-thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
    },
    "coil_temp": {
        "dp_id": 103,
        "code": "OCT1",
        "name": "Coil Temperature",
        "unit": "°C",
        "icon": "mdi:thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
    },
    "discharge_temp": {
        "dp_id": 104,
        "code": "CTT",
        "name": "Discharge Temperature",
        "unit": "°C",
        "icon": "mdi:thermometer-alert",
        "device_class": "temperature",
        "state_class": "measurement",
    },
    "return_air_temp": {
        "dp_id": 105,
        "code": "ReturnAirTemp",
        "name": "Suction Temperature",
        "unit": "°C",
        "icon": "mdi:thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
    },
    "water_tank_temp": {
        "dp_id": 106,
        "code": "WaterTankTemp",
        "name": "Water Tank Temperature",
        "unit": "°C",
        "icon": "mdi:water-thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
    },
    "post_throttle_temp": {
        "dp_id": 107,
        "code": "OCT_Cool",
        "name": "Post-Throttle Temperature",
        "unit": "°C",
        "icon": "mdi:thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
    },
    "water_in_temp": {
        "dp_id": 108,
        "code": "WaterInTemp",
        "name": "Water Inlet Temperature",
        "unit": "°C",
        "icon": "mdi:thermometer-water",
        "device_class": "temperature",
        "state_class": "measurement",
    },
    "water_out_temp": {
        "dp_id": 109,
        "code": "WaterOutTemp",
        "name": "Water Outlet Temperature",
        "unit": "°C",
        "icon": "mdi:thermometer-water",
        "device_class": "temperature",
        "state_class": "measurement",
    },
    "valve_front_temp": {
        "dp_id": 110,
        "code": "ValveFrontTemp",
        "name": "Valve Front Temperature",
        "unit": "°C",
        "icon": "mdi:thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
    },
    "valve_post_temp": {
        "dp_id": 111,
        "code": "ValvePostTemp",
        "name": "Valve Rear Temperature",
        "unit": "°C",
        "icon": "mdi:thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
    },
    # Fault Description (dp_id: 6) — decodes Tuya's 23-bit fault bitmap
    # (see typeSpec.label in the device model) into readable fault names
    # instead of the raw bitmap integer, listing all active faults if
    # more than one bit is set at once.
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
# BINARY SENSOR TYPES (read-only bool/bitmap - accessMode: "ro")
# ====================================================
BINARY_SENSOR_TYPES = {
    # Quick true/false view of the same DP as the "fault" sensor above —
    # same key is fine, separate dicts/platforms, no conflict.
    "fault": {
        "dp_id": 6,
        "code": "fault",
        "name": "Fault Status",
        "device_class": "problem",
        "conversion": "value != 0",
    },
    "compressor": {
        "dp_id": 112,
        "code": "Compressor",
        "name": "Compressor State",
        "device_class": "running",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']",
    },
    "four_way_valve": {
        "dp_id": 113,
        "code": "FouValve",
        "name": "Four-Way Valve",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']",
    },
    "aux_heater": {
        "dp_id": 114,
        "code": "Heat",
        "name": "Auxiliary Electric Heater",
        "device_class": "heat",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']",
    },
    "fan": {
        "dp_id": 115,
        "code": "Fan",
        "name": "Fan",
        "device_class": "running",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']",
    },
    "water_pump": {
        "dp_id": 116,
        "code": "Pumb",
        "name": "Water Pump",
        "device_class": "running",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']",
    },
    "chassis_heater": {
        "dp_id": 117,
        "code": "ChassisHeat",
        "name": "Chassis Heater",
        "device_class": "heat",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']",
    },
    "crankshaft_heater": {
        "dp_id": 118,
        "code": "CrankshaftHeat",
        "name": "Crankshaft Heater",
        "device_class": "heat",
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
        "min_value": 7.0,
        "max_value": 60.0,
        "step": 1.0,
        "api_conversion": "int(value)",
    },
    "temp_offset": {
        "dp_id": 101,
        "code": "Temp_Offset",
        "name": "Temperature Differential",
        "icon": "mdi:thermometer-lines",
        "unit": "°C",
        "min_value": 1.0,
        "max_value": 15.0,
        "step": 1.0,
        "api_conversion": "int(value)",
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
            "hot": "Heating",
            "cold": "Cooling",
            "auto": "Auto",
        },
    },
}
