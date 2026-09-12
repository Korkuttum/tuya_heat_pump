"""Model mapping for Mr. Silent FC25 / Aquara Pool Inverter Heat Pump (0000021mey)."""

MODEL_NAME = "Mr. Silent FC25 / Aquara Pool Inverter Heat Pump (0000021mey)"
# ====================================================
# Mr. Silent FC25 (Aquara Pool Inverter) @rolfsg
# ====================================================
# No raw DPs — same generic template as Ivapool (000004kb7r) and Pure
# Blue Onyx (f6ry00), but at this device's own unsuffixed dp_ids.

SENSOR_TYPES = {
    "temp_current": {
        "dp_id": 16,
        "code": "temp_current",
        "name": "Current Temperature",
        "unit": "°C",
        "icon": "mdi:thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
    },
    "compressor_strength": {
        "dp_id": 20,
        "code": "compressor_strength",
        "name": "Compressor Strength",
        "unit": "%",
        "icon": "mdi:gauge",
        "state_class": "measurement",
    },
    "temp_top": {
        "dp_id": 21,
        "code": "temp_top",
        "name": "Temperature Upper Limit",
        "unit": "°C",
        "icon": "mdi:thermometer-chevron-up",
        "device_class": "temperature",
        "state_class": "measurement",
    },
    "temp_bottom": {
        "dp_id": 22,
        "code": "temp_bottom",
        "name": "Temperature Lower Limit",
        "unit": "°C",
        "icon": "mdi:thermometer-chevron-down",
        "device_class": "temperature",
        "state_class": "measurement",
    },
    "temp_coiler": {
        "dp_id": 23,
        "code": "temp_coiler",
        "name": "Outdoor Coil Temperature",
        "unit": "°C",
        "icon": "mdi:thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
    },
    "temp_venting": {
        "dp_id": 24,
        "code": "temp_venting",
        "name": "Exhaust Temperature",
        "unit": "°C",
        "icon": "mdi:thermometer-alert",
        "device_class": "temperature",
        "state_class": "measurement",
    },
    "temp_effluent": {
        "dp_id": 25,
        "code": "temp_effluent",
        "name": "Outlet Water Temperature",
        "unit": "°C",
        "icon": "mdi:water-thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
    },
    "temp_around": {
        "dp_id": 26,
        "code": "temp_around",
        "name": "Ambient Temperature",
        "unit": "°C",
        "icon": "mdi:home-thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
    },
    "temp_inflow": {
        "dp_id": 102,
        "code": "temp_inflow",
        "name": "Inlet Water Temperature",
        "unit": "°C",
        "icon": "mdi:water-thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
    },
    "temp_return": {
        "dp_id": 103,
        "code": "temp_return",
        "name": "Return Gas Temperature",
        "unit": "°C",
        "icon": "mdi:thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
    },
    "temp_coiler_inside": {
        "dp_id": 104,
        "code": "temp_coiler_inside",
        "name": "Indoor Coil Temperature",
        "unit": "°C",
        "icon": "mdi:thermometer-lines",
        "device_class": "temperature",
        "state_class": "measurement",
    },
    "temp_radiator": {
        "dp_id": 105,
        "code": "temp_radiator",
        "name": "Radiator Temperature",
        "unit": "°C",
        "icon": "mdi:thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
    },
    "expansion_valve": {
        "dp_id": 106,
        "code": "expansion_valve",
        "name": "Expansion Valve Opening",
        "unit": "P",
        "icon": "mdi:pipe-valve",
        "state_class": "measurement",
    },
    "fault": {
        "dp_id": 15,
        "code": "fault",
        "name": "Fault Description",
        "icon": "mdi:alert-circle",
        "conversion": (
            "', '.join(n for b, n in [(1,'E1'),(2,'E2'),(4,'E3'),(8,'E4'),"
            "(16,'E5'),(32,'E6'),(64,'E7'),(128,'E8'),(256,'E9'),(512,'EA'),"
            "(1024,'EB'),(2048,'ED'),(4096,'P0'),(8192,'P1'),(16384,'P2'),"
            "(32768,'P3'),(65536,'P4'),(131072,'P5'),(262144,'P6'),"
            "(524288,'P7'),(1048576,'P8'),(2097152,'P9'),(4194304,'PA'),"
            "(8388608,'F1'),(16777216,'F2'),(33554432,'F3'),(67108864,'F4'),"
            "(134217728,'F5'),(268435456,'F6'),(536870912,'F7')"
            "] if value & b) or 'OK'"
        ),
    },
    "fault1": {
        "dp_id": 101,
        "code": "fault1",
        "name": "Extra Fault Description",
        "icon": "mdi:alert-circle-outline",
        "conversion": (
            "', '.join(n for b, n in [(1,'F8'),(2,'F9'),(4,'Fb'),(8,'Fa')]"
            " if value & b) or 'OK'"
        ),
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
    "fault1": {
        "dp_id": 101,
        "code": "fault1",
        "name": "Extra Fault Status",
        "device_class": "problem",
        "conversion": "value != 0",
    },
    "work_mode_option": {
        "dp_id": 107,
        "code": "work_mode_option",
        "name": "Work Mode Variant",
        "icon": "mdi:information-outline",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']",
        "options": {
            False: "3 Modes (Silence / Power / Boost)",
            True: "2 Modes (Silence / Power)",
        },
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
        "dp_id": 3,
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
        "dp_id": 4,
        "code": "temp_set",
        "name": "Temperature Setpoint",
        "icon": "mdi:thermostat",
        "unit": "°C",
        "min_value": -22.0,
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
        "dp_id": 2,
        "code": "mode",
        "name": "Mode",
        "icon": "mdi:hvac",
        "options": {
            "auto": "Auto",
            "heating": "Heating",
            "cold": "Cooling",
        },
    },
    "work_mode": {
        "dp_id": 5,
        "code": "work_mode",
        "name": "Work Mode",
        "icon": "mdi:cog",
        "options": {
            "power": "Power",
            "boost": "Boost",
            "silence": "Silence",
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
