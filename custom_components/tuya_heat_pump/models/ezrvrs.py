"""Model mapping for Aquatech X6 Heat Pump (ezrvrs)."""

MODEL_NAME = "Aquatech X6 Heat Pump (ezrvrs)"
# ====================================================
# Aquatech X6 320L @whoisjamesburke110011001100
#
# IMPORTANT: this device's Tuya `code` strings are extremely unreliable
# — many of them describe something completely different from what the
# DP actually is. Every entry below was named from the ACTUAL Chinese
# `name` field in Tuya's own device model, not from the (often
# misleading) code. A few notable examples of just how wrong the codes
# are on this device:
#   - "countdown_left"       is actually 电子膨胀阀 = Electronic Expansion
#                            Valve position, not a countdown/timer
#   - "work_state"           is actually 相序模块 = Phase Sequence Module
#                            (3-phase wiring check), not a work state
#   - "flow"                 is actually 风机状态 = Fan Status, not water
#                            flow
#   - "compressor_strength"  is actually 回气温度 = Return Gas
#                            Temperature, not compressor frequency
#   - "effluent_temp_f"      is actually 机组工装号 = Unit Assembly/
#                            Tooling Number — not a temperature at all
#   - "coiler_temp_f"        is actually 除霜前压机运行时间 = Compressor
#                            Runtime Before Defrost (minutes) — also
#                            not a temperature
#   - "draught_fan_state"    is actually 低压开关 = Low Pressure Switch
#   - "backwater"            is actually 水泵状态 = Water Pump Status
#   - "defrost_state"        is actually 高压开关 = High Pressure Switch
#   - "lpress"               is actually 电量检测 = Power Detection
# No raw-type DPs on this device — every field is a plain
# bool/value/enum/bitmap DP.
# ====================================================

SENSOR_TYPES = {
    "expansion_valve_position": {
        "dp_id": 14,
        "code": "countdown_left",
        "name": "Expansion Valve Position",
        "unit": "P",
        "icon": "mdi:valve",
    },
    # Fault Alarm (dp_id: 15) — this device's bitmap has 30 labels but
    # NO description text in Tuya's catalog (unlike the WOPOLTOP/Poolex
    # models), so there's nothing to decode individual bit meanings
    # from. Shown as the raw bitmap number for now.
    "fault": {
        "dp_id": 15,
        "code": "fault",
        "name": "Fault Alarm",
        "icon": "mdi:alert-circle",
    },
    "phase_sequence": {
        "dp_id": 17,
        "code": "work_state",
        "name": "Phase Sequence Module",
        "icon": "mdi:sine-wave",
    },
    "power_consumption": {
        "dp_id": 18,
        "code": "power_consumption",
        "name": "Today's Power Consumption",
        "unit": "kWh",
        "icon": "mdi:lightning-bolt",
        "device_class": "energy",
        "state_class": "total_increasing",
        "conversion": "value / 100",
    },
    "fan_status": {
        "dp_id": 19,
        "code": "flow",
        "name": "Fan Status",
        "icon": "mdi:fan",
    },
    "return_gas_temp": {
        "dp_id": 20,
        "code": "compressor_strength",
        "name": "Return Gas Temperature",
        "unit": "°C",
        "icon": "mdi:thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
    },
    "water_inlet_temp": {
        "dp_id": 21,
        "code": "temp_top",
        "name": "Water Inlet Temperature",
        "unit": "°C",
        "icon": "mdi:thermometer-water",
        "device_class": "temperature",
        "state_class": "measurement",
    },
    "water_outlet_temp": {
        "dp_id": 22,
        "code": "temp_bottom",
        "name": "Water Outlet Temperature",
        "unit": "°C",
        "icon": "mdi:thermometer-water",
        "device_class": "temperature",
        "state_class": "measurement",
    },
    "coil_temp": {
        "dp_id": 23,
        "code": "coiler_temp",
        "name": "Coil Temperature",
        "unit": "°C",
        "icon": "mdi:thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
    },
    "discharge_temp": {
        "dp_id": 24,
        "code": "venting_temp",
        "name": "Discharge Temperature",
        "unit": "°C",
        "icon": "mdi:thermometer-alert",
        "device_class": "temperature",
        "state_class": "measurement",
    },
    "ambient_temp": {
        "dp_id": 26,
        "code": "around_temp",
        "name": "Ambient Temperature",
        "unit": "°C",
        "icon": "mdi:home-thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
    },
    "unit_assembly_number": {
        "dp_id": 40,
        "code": "effluent_temp_f",
        "name": "Unit Assembly Number",
        "icon": "mdi:identifier",
    },
    "compressor_runtime_before_defrost": {
        "dp_id": 41,
        "code": "coiler_temp_f",
        "name": "Compressor Runtime Before Defrost",
        "unit": "min",
        "icon": "mdi:timer-sand",
        "device_class": "duration",
    },
    "current": {
        "dp_id": 101,
        "code": "cur_current",
        "name": "Current",
        "unit": "A",
        "icon": "mdi:current-ac",
        "device_class": "current",
        "state_class": "measurement",
        "conversion": "value / 1000",
    },
    "voltage": {
        "dp_id": 102,
        "code": "cur_voltage",
        "name": "Voltage",
        "unit": "V",
        "icon": "mdi:flash",
        "device_class": "voltage",
        "state_class": "measurement",
        "conversion": "value / 10",
    },
    "power": {
        "dp_id": 103,
        "code": "cur_power",
        "name": "Power",
        "unit": "W",
        "icon": "mdi:flash",
        "device_class": "power",
        "state_class": "measurement",
        "conversion": "value / 10",
    },
    "total_energy": {
        "dp_id": 104,
        "code": "electric_total",
        "name": "Total Power Consumption",
        "unit": "kWh",
        "icon": "mdi:lightning-bolt",
        "device_class": "energy",
        "state_class": "total_increasing",
        "conversion": "value / 100",
    },
}

# ====================================================
# BINARY SENSOR TYPES (read-only bool - accessMode: "ro")
# ====================================================
BINARY_SENSOR_TYPES = {
    "compressor_state": {
        "dp_id": 27,
        "code": "compressor_state",
        "name": "Compressor State",
        "device_class": "running",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']",
    },
    "four_way_valve": {
        "dp_id": 28,
        "code": "four_valve_state",
        "name": "Four-Way Valve",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']",
    },
    "low_pressure_switch": {
        "dp_id": 29,
        "code": "draught_fan_state",
        "name": "Low Pressure Switch",
        "device_class": "problem",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']",
    },
    "circulation_mode": {
        "dp_id": 30,
        "code": "pump_state",
        "name": "Refrigerant/Water Circulation",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']",
    },
    "water_pump": {
        "dp_id": 31,
        "code": "backwater",
        "name": "Water Pump Status",
        "device_class": "running",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']",
    },
    "electric_heating": {
        "dp_id": 32,
        "code": "ele_heating_state",
        "name": "Electric Heating State",
        "device_class": "heat",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']",
    },
    "high_pressure_switch": {
        "dp_id": 33,
        "code": "defrost_state",
        "name": "High Pressure Switch",
        "device_class": "problem",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']",
    },
    "power_detection": {
        "dp_id": 105,
        "code": "lpress",
        "name": "Power Detection",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']",
    },
    "linkage_switch": {
        "dp_id": 106,
        "code": "link",
        "name": "Linkage Switch",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']",
    },
    "water_flow_switch": {
        "dp_id": 107,
        "code": "flowswitch",
        "name": "Water Flow Switch",
        "device_class": "problem",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']",
    },
    "dip_switch_1": {
        "dp_id": 108,
        "code": "sw1",
        "name": "DIP Switch 1",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']",
    },
    "dip_switch_2": {
        "dp_id": 109,
        "code": "sw2",
        "name": "DIP Switch 2",
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
    # dp_id 7 is genuinely "rw" (unlike dp33's read-only pressure
    # switch above) — this looks like an actual writable defrost
    # trigger/override, not just a passive status flag.
    "defrost": {
        "dp_id": 7,
        "code": "defrost",
        "name": "Defrosting",
        "icon": "mdi:snowflake-melt",
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
        "name": "Target Temperature",
        "icon": "mdi:thermostat",
        "unit": "°C",
        "min_value": 15.0,
        "max_value": 75.0,
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
            "Stand": "Standby",
            "ECO": "Eco",
            "HYB": "Hybrid",
            "HYB1": "Hybrid 1",
            "ELE": "Electric",
        },
    },
}
