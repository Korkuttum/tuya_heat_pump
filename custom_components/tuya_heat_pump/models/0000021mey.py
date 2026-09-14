"""Model mapping for Mr. Silent FC25 / Aquara Pool Inverter Heat Pump (0000021mey)."""

MODEL_NAME = "Mr. Silent FC25 / Aquara Pool Inverter Heat Pump (0000021mey)"
# ====================================================
# Mr. Silent FC25 (Aquara Pool Inverter) @rolfsg
# ====================================================
# No raw DPs — same generic template as Ivapool (000004kb7r) and Pure
# Blue Onyx (f6ry00), but at this device's own unsuffixed dp_ids.
#
# Fault code descriptions (dp 15 / dp 101) contributed by @rolfsg from
# his unit's manual — covers 29 of the 30 dp 15 codes and all 4 dp 101
# codes; E9 has no known description yet so it's shown as a bare code.

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
    # Fault Description (dp_id: 15) — descriptions contributed by @rolfsg
    # from his unit's manual.
    "fault": {
        "dp_id": 15,
        "code": "fault",
        "name": "Fault Description",
        "icon": "mdi:alert-circle",
        "conversion": (
            "', '.join(n for b, n in ["
            "(1,'E1: High pressure protection'),"
            "(2,'E2: Low pressure protection'),"
            "(4,'E3: No water protection'),"
            "(8,'E4: 3-phase sequence protection'),"
            "(16,'E5: Power supply exceeds operation range (not failure)'),"
            "(32,'E6: Excessive temp difference between inlet and outlet water'),"
            "(64,'E7: Water outlet temp too high or too low protection'),"
            "(128,'E8: High exhaust temp protection'),"
            "(256,'E9'),"
            "(512,'EA: Heat exchanger overheat protection'),"
            "(1024,'EB: Ambient temperature too high or too low protection (not failure)'),"
            "(2048,'ED: Anti-freezing reminder'),"
            "(4096,'P0: Controller communication failure'),"
            "(8192,'P1: Water inlet temp sensor failure'),"
            "(16384,'P2: Water outlet temp sensor failure'),"
            "(32768,'P3: Gas exhaust temp sensor failure'),"
            "(65536,'P4: Evaporator coil pipe temp sensor failure'),"
            "(131072,'P5: Gas return temp sensor failure'),"
            "(262144,'P6: Cooling coil temp sensor failure'),"
            "(524288,'P7: Ambient temp sensor failure'),"
            "(1048576,'P8: Cooling plate temp sensor failure'),"
            "(2097152,'P9: Current sensor failure'),"
            "(4194304,'PA: Restart memory failure'),"
            "(8388608,'F1: Compressor driver module failure'),"
            "(16777216,'F2: PFC module failure'),"
            "(33554432,'F3: Compressor start failure'),"
            "(67108864,'F4: Compressor running failure'),"
            "(134217728,'F5: Inverter board over-current protection'),"
            "(268435456,'F6: Inverter board over-heat protection'),"
            "(536870912,'F7: Current protection')"
            "] if value & b) or 'OK'"
        ),
    },
    # Extra Fault Description (dp_id: 101) — descriptions contributed by
    # @rolfsg from his unit's manual.
    "fault1": {
        "dp_id": 101,
        "code": "fault1",
        "name": "Extra Fault Description",
        "icon": "mdi:alert-circle-outline",
        "conversion": (
            "', '.join(n for b, n in ["
            "(1,'F8: Cooling plate over-heat protection'),"
            "(2,'F9: Fan motor failure'),"
            "(4,'Fb: Power filter plate no-power protection'),"
            "(8,'FA: PFC module over-current protection')"
            "] if value & b) or 'OK'"
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
