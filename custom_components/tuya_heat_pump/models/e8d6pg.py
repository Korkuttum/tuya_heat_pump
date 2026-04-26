"""Model mapping for Ecologic Ecopool Heat Pump (e8d6pg)."""

MODEL_NAME = "Ecologic Ecopool Heat Pump (e8d6pg)"
# ====================================================
# Ecologic Ecopool @danilofborges
# ====================================================
SENSOR_TYPES = {
    # ========== TEMPERATURE SENSORS ==========
    "temp_current": {
        "dp_id": 3,
        "code": "temp_current",
        "name": "Current Temperature",
        "unit": "°C",
        "icon": "mdi:thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
    },
    "AmbientTemp": {
        "dp_id": 102,
        "code": "AmbientTemp",
        "name": "Ambient Temperature",
        "unit": "°C",
        "icon": "mdi:home-thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
    },
    "OCT1": {
        "dp_id": 103,
        "code": "OCT1",
        "name": "Coil Temperature",
        "unit": "°C",
        "icon": "mdi:thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
    },
    "CTT": {
        "dp_id": 104,
        "code": "CTT",
        "name": "Discharge Temperature",
        "unit": "°C",
        "icon": "mdi:thermometer-alert",
        "device_class": "temperature",
        "state_class": "measurement",
    },
    "ReturnAirTemp": {
        "dp_id": 105,
        "code": "ReturnAirTemp",
        "name": "Suction Temperature",
        "unit": "°C",
        "icon": "mdi:thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
    },
    "WaterTankTemp": {
        "dp_id": 106,
        "code": "WaterTankTemp",
        "name": "Water Tank Temperature",
        "unit": "°C",
        "icon": "mdi:water-thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
    },
    "OCT_Cool": {
        "dp_id": 107,
        "code": "OCT_Cool",
        "name": "Post-Throttle Temperature",
        "unit": "°C",
        "icon": "mdi:thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
    },
    "WaterInTemp": {
        "dp_id": 108,
        "code": "WaterInTemp",
        "name": "Inlet Water Temperature",
        "unit": "°C",
        "icon": "mdi:thermometer-water",
        "device_class": "temperature",
        "state_class": "measurement",
    },
    "WaterOutTemp": {
        "dp_id": 109,
        "code": "WaterOutTemp",
        "name": "Outlet Water Temperature",
        "unit": "°C",
        "icon": "mdi:thermometer-water",
        "device_class": "temperature",
        "state_class": "measurement",
    },
    "ValveFrontTemp": {
        "dp_id": 110,
        "code": "ValveFrontTemp",
        "name": "Valve Front Temperature",
        "unit": "°C",
        "icon": "mdi:thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
    },
    "ValvePostTemp": {
        "dp_id": 111,
        "code": "ValvePostTemp",
        "name": "Valve Post Temperature",
        "unit": "°C",
        "icon": "mdi:thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
    },
    
    # ========== SETPOINTS (read-only for display) ==========
    "temp_set": {
        "dp_id": 2,
        "code": "temp_set",
        "name": "Temperature Setpoint",
        "unit": "°C",
        "icon": "mdi:thermostat",
        "device_class": "temperature",
        "state_class": "measurement",
    },
    "Temp_Offset": {
        "dp_id": 101,
        "code": "Temp_Offset",
        "name": "Temperature Offset",
        "unit": "°C",
        "icon": "mdi:thermometer-plus",
        "device_class": "temperature",
        "state_class": "measurement",
    },
}

# ====================================================
# BINARY SENSOR TYPES (read-only bool/bitmap - accessMode: "ro")
# ====================================================
BINARY_SENSOR_TYPES = {
    "fault": {
        "dp_id": 6,
        "code": "fault",
        "name": "Fault Alarm",
        "icon": "mdi:alert-circle",
        "device_class": "problem",
        "conversion": "value != 0"
    },
    "Compressor": {
        "dp_id": 112,
        "code": "Compressor",
        "name": "Compressor",
        "icon": "mdi:engine",
        "device_class": "running",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']"
    },
    "FouValve": {
        "dp_id": 113,
        "code": "FouValve",
        "name": "Four-Way Valve",
        "icon": "mdi:valve",
        "device_class": "opening",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']"
    },
    "Heat": {
        "dp_id": 114,
        "code": "Heat",
        "name": "Auxiliary Electric Heater",
        "icon": "mdi:heating-coil",
        "device_class": "heat",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']"
    },
    "Fan": {
        "dp_id": 115,
        "code": "Fan",
        "name": "Fan",
        "icon": "mdi:fan",
        "device_class": "running",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']"
    },
    "Pumb": {
        "dp_id": 116,
        "code": "Pumb",
        "name": "Water Pump",
        "icon": "mdi:water-pump",
        "device_class": "running",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']"
    },
    "ChassisHeat": {
        "dp_id": 117,
        "code": "ChassisHeat",
        "name": "Chassis Heater",
        "icon": "mdi:heating-coil",
        "device_class": "heat",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']"
    },
    "CrankshaftHeat": {
        "dp_id": 118,
        "code": "CrankshaftHeat",
        "name": "Crankshaft Heater",
        "icon": "mdi:heating-coil",
        "device_class": "heat",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']"
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
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']"
    },
}

# ====================================================
# NUMBER TYPES (read-write value - accessMode: "rw")
# ====================================================
NUMBER_TYPES = {
    "temp_set": {
        "dp_id": 2,
        "code": "temp_set",
        "name": "Temperature Setpoint",
        "icon": "mdi:thermostat",
        "unit": "°C",
        "min_value": 8.0,
        "max_value": 40.0,
        "step": 1.0,
        "api_conversion": "value / 10"
    },
    "Temp_Offset": {
        "dp_id": 101,
        "code": "Temp_Offset",
        "name": "Temperature Offset",
        "icon": "mdi:thermometer-plus",
        "unit": "°C",
        "min_value": 1.0,
        "max_value": 15.0,
        "step": 1.0,
        "api_conversion": "value / 10"
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
            "eco": "ECO"
        },
    },
}
