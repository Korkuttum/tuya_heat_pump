"""Model mapping for Kensol Heat Pump (modelId: fdru4s)."""

MODEL_NAME = "Kensol Heat Pump (fdru4s)"
# ====================================================
# Kensol Heat Pump @VaporX25
# modelId: fdru4s
# DP map sourced from /v2.0/cloud/thing/{id}/shadow/properties + /model
# Notes:
#   - temp_current (dp 16) and temp_current_f (dp 35) return sentinel values
#     (-30 / -22) on this device; the real live temperatures are packed inside
#     status_pg_1 (dp 101) as int32 fields. Kept temp_current for older users
#     but the raw-decoded sensors below are the ones to trust.
#   - status_pg_1 raw payload decoded field mapping was contributed by @VaporX25
#     using the raw_explorer.py tool. Encoding: int32 big-endian, signed.
#   - fault (dp 15) is a 29-bit bitmap (Er03..Er70). Exposed as binary sensor.
#   - fan_module_fault_1/2 (dp 196/197) and custom_fault_bit (dp 199) are
#     integer fault register bitmaps, exposed as binary "any error" sensors.
#   - mode (dp 2) = frequency profile (smart/strong/mute).
#     work_mode (dp 5) = HVAC mode (heat/cool/auto).
#   - temp_set (dp 4) mirrors the setpoint of the active work_mode;
#     heat/cool/auto_temp_set (dp 151/152/153) are per-mode setpoints.
#   - reset (dp 198) is write-only, not exposed.
# ====================================================

SENSOR_TYPES = {
    # ---- Raw-field sensors from status_pg_1 (dp 101) ----
    # Contributed and verified by @VaporX25 against the Smart Life app.
    "water_inlet_temperature": {
        "dp_id": 101,
        "code": "water_inlet_temperature",
        "raw_source": "status_pg_1",
        "field_index": 0,
        "encoding": "int32_be",
        "name": "Water Inlet Temperature",
        "unit": "°C",
        "icon": "mdi:pool-thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
    },
    "water_outlet_temperature": {
        "dp_id": 101,
        "code": "water_outlet_temperature",
        "raw_source": "status_pg_1",
        "field_index": 1,
        "encoding": "int32_be",
        "name": "Water Outlet Temperature",
        "unit": "°C",
        "icon": "mdi:water-thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
    },
    "ambient_temperature": {
        "dp_id": 101,
        "code": "ambient_temperature",
        "raw_source": "status_pg_1",
        "field_index": 2,
        "encoding": "int32_be",
        "name": "Ambient Temperature",
        "unit": "°C",
        "icon": "mdi:home-thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
    },
    "exhaust_gas_temperature": {
        "dp_id": 101,
        "code": "exhaust_gas_temperature",
        "raw_source": "status_pg_1",
        "field_index": 3,
        "encoding": "int32_be",
        "name": "Exhaust Gas Temperature",
        "unit": "°C",
        "icon": "mdi:thermometer-alert",
        "device_class": "temperature",
        "state_class": "measurement",
    },
    "return_gas_temperature": {
        "dp_id": 101,
        "code": "return_gas_temperature",
        "raw_source": "status_pg_1",
        "field_index": 4,
        "encoding": "int32_be",
        "name": "Return Gas Temperature",
        "unit": "°C",
        "icon": "mdi:thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
    },
    "evaporator_coil_temperature": {
        "dp_id": 101,
        "code": "evaporator_coil_temperature",
        "raw_source": "status_pg_1",
        "field_index": 5,
        "encoding": "int32_be",
        "name": "Evaporator Coil Temperature",
        "unit": "°C",
        "icon": "mdi:thermometer-lines",
        "device_class": "temperature",
        "state_class": "measurement",
    },
    "inner_coil_temperature": {
        "dp_id": 101,
        "code": "inner_coil_temperature",
        "raw_source": "status_pg_1",
        "field_index": 6,
        "encoding": "int32_be",
        "name": "Inner Coil Temperature",
        "unit": "°C",
        "icon": "mdi:thermometer-lines",
        "device_class": "temperature",
        "state_class": "measurement",
    },
    "main_expansion_valve_opening": {
        "dp_id": 101,
        "code": "main_expansion_valve_opening",
        "raw_source": "status_pg_1",
        "field_index": 8,
        "encoding": "int32_be",
        "name": "Main Expansion Valve Opening",
        "unit": "P",
        "icon": "mdi:pipe-valve",
        "state_class": "measurement",
    },
    "compressor_current": {
        "dp_id": 101,
        "code": "compressor_current",
        "raw_source": "status_pg_1",
        "field_index": 10,
        "encoding": "int32_be",
        "name": "Compressor Current",
        "unit": "A",
        "icon": "mdi:current-ac",
        "device_class": "current",
        "state_class": "measurement",
    },
    "heat_sink_temperature": {
        "dp_id": 101,
        "code": "heat_sink_temperature",
        "raw_source": "status_pg_1",
        "field_index": 11,
        "encoding": "int32_be",
        "name": "Heat Sink Temperature",
        "unit": "°C",
        "icon": "mdi:thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
    },
    "dc_bus_voltage": {
        "dp_id": 101,
        "code": "dc_bus_voltage",
        "raw_source": "status_pg_1",
        "field_index": 12,
        "encoding": "int32_be",
        "name": "DC Bus Voltage",
        "unit": "V",
        "icon": "mdi:lightning-bolt",
        "device_class": "voltage",
        "state_class": "measurement",
    },
    "compressor_frequency": {
        "dp_id": 101,
        "code": "compressor_frequency",
        "raw_source": "status_pg_1",
        "field_index": 13,
        "encoding": "int32_be",
        "name": "Compressor Frequency",
        "unit": "Hz",
        "icon": "mdi:cosine-wave",
        "device_class": "frequency",
        "state_class": "measurement",
    },
    "dc_fan_1_speed": {
        "dp_id": 101,
        "code": "dc_fan_1_speed",
        "raw_source": "status_pg_1",
        "field_index": 14,
        "encoding": "int32_be",
        "name": "DC Fan 1 Speed",
        "unit": "rpm",
        "icon": "mdi:fan",
        "state_class": "measurement",
    },

    # ---- Regular DP sensors ----
    # temp_current returns -30°C sentinel on this device (probe not wired
    # to the DP); real inlet temp is water_inlet_temperature above.
    "temp_current": {
        "dp_id": 16,
        "code": "temp_current",
        "name": "Current Temperature (raw DP)",
        "unit": "°C",
        "icon": "mdi:thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
    },
    "temp_current_f": {
        "dp_id": 35,
        "code": "temp_current_f",
        "name": "Current Temperature (°F, raw DP)",
        "unit": "°F",
        "icon": "mdi:thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
    },
}

BINARY_SENSOR_TYPES = {
    "fault": {
        "dp_id": 15,
        "code": "fault",
        "name": "Fault Alarm",
        "device_class": "problem",
        "conversion": "value != 0"
    },
    "fan_module_fault_1": {
        "dp_id": 196,
        "code": "fan_module_fault_1",
        "name": "Fan Module 1 Fault",
        "device_class": "problem",
        "conversion": "value != 0"
    },
    "fan_module_fault_2": {
        "dp_id": 197,
        "code": "fan_module_fault_2",
        "name": "Fan Module 2 Fault",
        "device_class": "problem",
        "conversion": "value != 0"
    },
    "custom_fault_bit": {
        "dp_id": 199,
        "code": "custom_fault_bit",
        "name": "Inverter Module Fault",
        "device_class": "problem",
        "conversion": "value != 0"
    },
}

SWITCH_TYPES = {
    "switch": {
        "dp_id": 1,
        "code": "switch",
        "name": "Power",
        "icon": "mdi:power",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']"
    },
}

NUMBER_TYPES = {
    "temp_set": {
        "dp_id": 4,
        "code": "temp_set",
        "name": "Target Temperature",
        "icon": "mdi:thermometer",
        "unit": "°C",
        "min_value": 10.0,
        "max_value": 75.0,
        "step": 1.0,
        "conversion": "value",
        "api_conversion": "round(value)"
    },
    "heat_temp_set": {
        "dp_id": 151,
        "code": "heat_temp_set",
        "name": "Heat Mode Setpoint",
        "icon": "mdi:thermometer-plus",
        "unit": "°C",
        "min_value": 5.0,
        "max_value": 75.0,
        "step": 1.0,
        "conversion": "value",
        "api_conversion": "round(value)"
    },
    "cool_temp_set": {
        "dp_id": 152,
        "code": "cool_temp_set",
        "name": "Cool Mode Setpoint",
        "icon": "mdi:thermometer-minus",
        "unit": "°C",
        "min_value": 8.0,
        "max_value": 40.0,
        "step": 1.0,
        "conversion": "value",
        "api_conversion": "round(value)"
    },
    "auto_temp_set": {
        "dp_id": 153,
        "code": "auto_temp_set",
        "name": "Auto Mode Setpoint",
        "icon": "mdi:thermometer-auto",
        "unit": "°C",
        "min_value": 8.0,
        "max_value": 40.0,
        "step": 1.0,
        "conversion": "value",
        "api_conversion": "round(value)"
    },
}

SELECT_TYPES = {
    "work_mode": {
        "dp_id": 5,
        "code": "work_mode",
        "name": "Work Mode",
        "icon": "mdi:hvac",
        "options": {
            "heat": "Heat",
            "cool": "Cool",
            "auto": "Auto"
        },
    },
    "mode": {
        "dp_id": 2,
        "code": "mode",
        "name": "Frequency Mode",
        "icon": "mdi:speedometer",
        "options": {
            "smart": "Smart",
            "strong": "Strong",
            "mute": "Silent"
        },
    },
    "temp_unit_convert": {
        "dp_id": 6,
        "code": "temp_unit_convert",
        "name": "Temperature Unit",
        "icon": "mdi:thermometer",
        "options": {
            "c": "Celsius",
            "f": "Fahrenheit"
        },
    },
}
