"""Model mapping for Effecta Air-IQ R290 Heat Pump (e1nde5gc)."""

MODEL_NAME = "Effecta Air-IQ R290 Heat Pump (e1nde5gc)"
# ====================================================
# Effecta Air-IQ R290 @mnoxfeld
# ====================================================
# Product code PW58382-4; same Power World OEM family as e1k5wjuc.
# pg120_status (dp 101) confirmed int16_be and field-mapped by @mnoxfeld
# via raw_explorer.py, verified against the Smart Life app. wth_set/
# heating_set ranges confirmed on the real device; cooling_set still
# untested (kept at Tuya's own typeSpec range). reset/hdef kept even
# though @mnoxfeld's own contribution dropped them, for anyone who wants
# them (hide the entities individually in HA if unwanted).

# ====================================================
# SENSOR TYPES (read-only value - accessMode: "ro")
# ====================================================
SENSOR_TYPES = {
    # ---- pg120_status (dp 101) — live system telemetry, @mnoxfeld ----
    "water_inlet_temperature": {
        "dp_id": 101,
        "code": "water_inlet_temperature",
        "raw_source": "pg120_status",
        "field_index": 0,
        "encoding": "int16_be",
        "name": "Water Inlet Temperature",
        "unit": "°C",
        "icon": "mdi:water-thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
    },
    "water_outlet_temperature": {
        "dp_id": 101,
        "code": "water_outlet_temperature",
        "raw_source": "pg120_status",
        "field_index": 1,
        "encoding": "int16_be",
        "name": "Water Outlet Temperature",
        "unit": "°C",
        "icon": "mdi:water-thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
    },
    "exhaust_gas_temperature": {
        "dp_id": 101,
        "code": "exhaust_gas_temperature",
        "raw_source": "pg120_status",
        "field_index": 2,
        "encoding": "int16_be",
        "name": "Exhaust Gas Temperature",
        "unit": "°C",
        "icon": "mdi:thermometer-alert",
        "device_class": "temperature",
        "state_class": "measurement",
    },
    "return_gas_temperature": {
        "dp_id": 101,
        "code": "return_gas_temperature",
        "raw_source": "pg120_status",
        "field_index": 3,
        "encoding": "int16_be",
        "name": "Return Gas Temperature",
        "unit": "°C",
        "icon": "mdi:thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
    },
    "evaporator_coil_temperature": {
        "dp_id": 101,
        "code": "evaporator_coil_temperature",
        "raw_source": "pg120_status",
        "field_index": 4,
        "encoding": "int16_be",
        "name": "Evaporator Coil Temperature",
        "unit": "°C",
        "icon": "mdi:thermometer-lines",
        "device_class": "temperature",
        "state_class": "measurement",
    },
    # Field index 6 skipped — unused/unidentified.
    "opening_steps_main_exp_valve": {
        "dp_id": 101,
        "code": "opening_steps_main_exp_valve",
        "raw_source": "pg120_status",
        "field_index": 5,
        "encoding": "int16_be",
        "name": "Main Expansion Valve Opening",
        "unit": "step",
        "icon": "mdi:pipe-valve",
        "state_class": "measurement",
    },
    "compressor_actual_frequency": {
        "dp_id": 101,
        "code": "compressor_actual_frequency",
        "raw_source": "pg120_status",
        "field_index": 7,
        "encoding": "int16_be",
        "name": "Compressor Actual Frequency",
        "unit": "Hz",
        "icon": "mdi:cosine-wave",
        "device_class": "frequency",
        "state_class": "measurement",
    },
    "low_pressure_conversion_temp": {
        "dp_id": 101,
        "code": "low_pressure_conversion_temp",
        "raw_source": "pg120_status",
        "field_index": 8,
        "encoding": "int16_be",
        "name": "Low Pressure Conversion Temperature",
        "unit": "°C",
        "icon": "mdi:thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
    },
    "fan1_wind_speed": {
        "dp_id": 101,
        "code": "fan1_wind_speed",
        "raw_source": "pg120_status",
        "field_index": 9,
        "encoding": "int16_be",
        "name": "Fan 1 Speed",
        "unit": "rpm",
        "icon": "mdi:fan",
        "state_class": "measurement",
    },
    "current_water_flow_rate": {
        "dp_id": 101,
        "code": "current_water_flow_rate",
        "raw_source": "pg120_status",
        "field_index": 10,
        "encoding": "int16_be",
        "conversion": "value / 100",
        "name": "Water Flow Rate",
        "unit": "m³/h",
        "icon": "mdi:water-pump",
        "state_class": "measurement",
    },
    "total_power_of_heatpump": {
        "dp_id": 101,
        "code": "total_power_of_heatpump",
        "raw_source": "pg120_status",
        "field_index": 11,
        "encoding": "int16_be",
        "name": "Heat Pump Power",
        "unit": "W",
        "icon": "mdi:flash",
        "device_class": "power",
        "state_class": "measurement",
    },
    "ambient_temperature": {
        "dp_id": 101,
        "code": "ambient_temperature",
        "raw_source": "pg120_status",
        "field_index": 12,
        "encoding": "int16_be",
        "name": "Ambient Temperature",
        "unit": "°C",
        "icon": "mdi:home-thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
    },
    "total_effluent_temperature": {
        "dp_id": 101,
        "code": "total_effluent_temperature",
        "raw_source": "pg120_status",
        "field_index": 13,
        "encoding": "int16_be",
        "name": "Total Effluent Temperature",
        "unit": "°C",
        "icon": "mdi:thermometer-water",
        "device_class": "temperature",
        "state_class": "measurement",
    },
    "cooling_coil_temperature": {
        "dp_id": 101,
        "code": "cooling_coil_temperature",
        "raw_source": "pg120_status",
        "field_index": 14,
        "encoding": "int16_be",
        "name": "Cooling Coil Temperature",
        "unit": "°C",
        "icon": "mdi:thermometer-lines",
        "device_class": "temperature",
        "state_class": "measurement",
    },
    "water_tank_temperature": {
        "dp_id": 101,
        "code": "water_tank_temperature",
        "raw_source": "pg120_status",
        "field_index": 15,
        "encoding": "int16_be",
        "name": "Water Tank Temperature",
        "unit": "°C",
        "icon": "mdi:water-thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
    },
    "compressor_current": {
        "dp_id": 101,
        "code": "compressor_current",
        "raw_source": "pg120_status",
        "field_index": 16,
        "encoding": "int16_be",
        "name": "Compressor Current",
        "unit": "A",
        "icon": "mdi:current-ac",
        "device_class": "current",
        "state_class": "measurement",
    },
    "heat_sink_temperature": {
        "dp_id": 101,
        "code": "heat_sink_temperature",
        "raw_source": "pg120_status",
        "field_index": 17,
        "encoding": "int16_be",
        "name": "Heat Sink Temperature",
        "unit": "°C",
        "icon": "mdi:thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
    },
    "frequency_of_press_operation": {
        "dp_id": 101,
        "code": "frequency_of_press_operation",
        "raw_source": "pg120_status",
        "field_index": 18,
        "encoding": "int16_be",
        "name": "Frequency of Press Operation",
        "unit": "Hz",
        "icon": "mdi:cosine-wave",
        "device_class": "frequency",
        "state_class": "measurement",
    },
    "low_pressure_sensor_value": {
        "dp_id": 101,
        "code": "low_pressure_sensor_value",
        "raw_source": "pg120_status",
        "field_index": 19,
        "encoding": "int16_be",
        "conversion": "value / 100",
        "name": "Low Pressure Sensor",
        "unit": "bar",
        "icon": "mdi:gauge",
        "device_class": "pressure",
        "state_class": "measurement",
    },
    # Field index 20 skipped — unused/unidentified.
    # EUV/SG grid signals — kept as-is, no unit; user can rename if their
    # utility/grid setup exposes what these actually mean.
    "euv_powered_signal": {
        "dp_id": 101,
        "code": "euv_powered_signal",
        "raw_source": "pg120_status",
        "field_index": 21,
        "encoding": "int16_be",
        "name": "EUV Powered Signal",
        "icon": "mdi:signal",
    },
    "sg_grid_signal": {
        "dp_id": 101,
        "code": "sg_grid_signal",
        "raw_source": "pg120_status",
        "field_index": 22,
        "encoding": "int16_be",
        "name": "SG Grid Signal",
        "icon": "mdi:signal",
    },
    "refrigerant_concentration": {
        "dp_id": 101,
        "code": "refrigerant_concentration",
        "raw_source": "pg120_status",
        "field_index": 23,
        "encoding": "int16_be",
        "name": "Refrigerant Concentration",
        "unit": "%",
        "icon": "mdi:percent",
        "state_class": "measurement",
    },
    "dc_bus_voltage_value": {
        "dp_id": 101,
        "code": "dc_bus_voltage_value",
        "raw_source": "pg120_status",
        "field_index": 24,
        "encoding": "int16_be",
        "name": "DC Bus Voltage",
        "unit": "V",
        "icon": "mdi:lightning-bolt",
        "device_class": "voltage",
        "state_class": "measurement",
    },
    "target_speed_dc_water_pump": {
        "dp_id": 101,
        "code": "target_speed_dc_water_pump",
        "raw_source": "pg120_status",
        "field_index": 25,
        "encoding": "int16_be",
        "name": "Target DC Water Pump Speed",
        "unit": "%",
        "icon": "mdi:pump",
        "state_class": "measurement",
    },
    "actual_speed_dc_water_pump": {
        "dp_id": 101,
        "code": "actual_speed_dc_water_pump",
        "raw_source": "pg120_status",
        "field_index": 26,
        "encoding": "int16_be",
        "name": "Actual DC Water Pump Speed",
        "unit": "%",
        "icon": "mdi:pump",
        "state_class": "measurement",
    },

    # Fault Description (dp_id: 15) — Tuya's own schema for this device
    # lists a single bitmap label: Er09 (communication fault).
    "fault": {
        "dp_id": 15,
        "code": "fault",
        "name": "Fault Description",
        "icon": "mdi:alert-circle",
        "conversion": (
            "', '.join(n for b, n in [(1,'Er09')] if value & b) or 'OK'"
        ),
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
    # Fault Status (dp_id: 15)
    "fault": {
        "dp_id": 15,
        "code": "fault",
        "name": "Fault Status",
        "device_class": "problem",
        "conversion": "value != 0",
    },
}

# ====================================================
# SWITCH TYPES (read-write bool - accessMode: "rw"/"wr")
# ====================================================
SWITCH_TYPES = {
    # Power Switch (dp_id: 1)
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
    # Hot Water Temperature Setpoint (dp_id: 110) — range confirmed on
    # the real device by @mnoxfeld.
    "wth_set": {
        "dp_id": 110,
        "code": "wth_set",
        "name": "Hot Water Temperature",
        "icon": "mdi:water-thermometer",
        "unit": "°C",
        "min_value": 28.0,
        "max_value": 65.0,
        "step": 1.0,
        "api_conversion": "value",
    },
    # Heating Temperature Setpoint (dp_id: 111) — range confirmed on the
    # real device by @mnoxfeld.
    "heating_set": {
        "dp_id": 111,
        "code": "heating_set",
        "name": "Heating Temperature",
        "icon": "mdi:thermostat",
        "unit": "°C",
        "min_value": 15.0,
        "max_value": 70.0,
        "step": 1.0,
        "api_conversion": "value",
    },
    # Cooling Temperature Setpoint (dp_id: 112) — still Tuya's own
    # typeSpec range, not yet confirmed against a real device.
    "cooling_set": {
        "dp_id": 112,
        "code": "cooling_set",
        "name": "Cooling Temperature",
        "icon": "mdi:snowflake",
        "unit": "°C",
        "min_value": 7.0,
        "max_value": 86.0,
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
    # Operation Mode (dp_id: 2) - smart, strong, mute
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
    # Work Mode (dp_id: 5) - wth, heat, cool, wth_heat, wth_cool
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
    # Temperature Unit (dp_id: 6) - c, f
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
