"""Model mapping for Power World R290 Full DC Heat Pump (e1k5wjuc)."""

MODEL_NAME = "Power World R290 Full DC Heat Pump (e1k5wjuc)"
# ====================================================
# Power World R290 Full DC @tomoo777
# Raw payload mapping contributed and verified against the Smart Life app
# by @tomoo777 using raw_explorer.py. All raw fields are 20 × signed
# big-endian int32 (4 bytes each). Some fields need scaling — those are
# applied via `conversion` below (values are always divisors of the raw int).
#
# Skipped intentionally:
#   - status_parameter_group_1 field indices 18-19 (EUV/SG grid signals):
#     kept as-is, no unit; user can rename if their unit exposes them.
#   - parameter_group_23 field indices 11-16 (device clock year/month/day/
#     hour/min/sec): not useful as separate sensors. Users can build a
#     template sensor if they want a "last device update" timestamp.
#   - parameter_group_1..10 (dp 118-128): configuration/settings, not live
#     sensors. Can be mapped later if needed.
# ====================================================

# ====================================================
# SENSOR TYPES (read-only value - accessMode: "ro")
# ====================================================
SENSOR_TYPES = {
    # ---- status_parameter_group_1 (dp 101) — live system telemetry ----
    "water_inlet_temperature": {
        "dp_id": 101,
        "code": "water_inlet_temperature",
        "raw_source": "status_parameter_group_1",
        "field_index": 0,
        "encoding": "int32_be",
        "name": "Water Inlet Temperature",
        "unit": "°C",
        "icon": "mdi:water-thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
    },
    "water_outlet_temperature": {
        "dp_id": 101,
        "code": "water_outlet_temperature",
        "raw_source": "status_parameter_group_1",
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
        "raw_source": "status_parameter_group_1",
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
        "raw_source": "status_parameter_group_1",
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
        "raw_source": "status_parameter_group_1",
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
        "raw_source": "status_parameter_group_1",
        "field_index": 5,
        "encoding": "int32_be",
        "name": "Evaporator Coil Temperature",
        "unit": "°C",
        "icon": "mdi:thermometer-lines",
        "device_class": "temperature",
        "state_class": "measurement",
    },
    "cooling_coil_temperature": {
        "dp_id": 101,
        "code": "cooling_coil_temperature",
        "raw_source": "status_parameter_group_1",
        "field_index": 6,
        "encoding": "int32_be",
        "name": "Cooling Coil Temperature",
        "unit": "°C",
        "icon": "mdi:thermometer-lines",
        "device_class": "temperature",
        "state_class": "measurement",
    },
    "water_tank_temperature": {
        "dp_id": 101,
        "code": "water_tank_temperature",
        "raw_source": "status_parameter_group_1",
        "field_index": 7,
        "encoding": "int32_be",
        "name": "Water Tank Temperature",
        "unit": "°C",
        "icon": "mdi:water-thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
    },
    "main_expansion_valve_opening": {
        "dp_id": 101,
        "code": "main_expansion_valve_opening",
        "raw_source": "status_parameter_group_1",
        "field_index": 8,
        "encoding": "int32_be",
        "name": "Main Expansion Valve Opening",
        "unit": "P",
        "icon": "mdi:pipe-valve",
        "state_class": "measurement",
    },
    "auxiliary_expansion_valve_opening": {
        "dp_id": 101,
        "code": "auxiliary_expansion_valve_opening",
        "raw_source": "status_parameter_group_1",
        "field_index": 9,
        "encoding": "int32_be",
        "name": "Auxiliary Expansion Valve Opening",
        "unit": "P",
        "icon": "mdi:pipe-valve",
        "state_class": "measurement",
    },
    "compressor_current": {
        "dp_id": 101,
        "code": "compressor_current",
        "raw_source": "status_parameter_group_1",
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
        "raw_source": "status_parameter_group_1",
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
        "raw_source": "status_parameter_group_1",
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
        "raw_source": "status_parameter_group_1",
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
        "raw_source": "status_parameter_group_1",
        "field_index": 14,
        "encoding": "int32_be",
        "name": "DC Fan 1 Speed",
        "unit": "rpm",
        "icon": "mdi:fan",
        "state_class": "measurement",
    },
    "dc_fan_2_speed": {
        "dp_id": 101,
        "code": "dc_fan_2_speed",
        "raw_source": "status_parameter_group_1",
        "field_index": 15,
        "encoding": "int32_be",
        "name": "DC Fan 2 Speed",
        "unit": "rpm",
        "icon": "mdi:fan",
        "state_class": "measurement",
    },
    "low_pressure_sensor": {
        "dp_id": 101,
        "code": "low_pressure_sensor",
        "raw_source": "status_parameter_group_1",
        "field_index": 16,
        "encoding": "int32_be",
        "name": "Low Pressure Sensor",
        "unit": "bar",
        "icon": "mdi:gauge",
        "device_class": "pressure",
        "state_class": "measurement",
    },
    "low_pressure_conversion_temperature": {
        "dp_id": 101,
        "code": "low_pressure_conversion_temperature",
        "raw_source": "status_parameter_group_1",
        "field_index": 17,
        "encoding": "int32_be",
        "name": "Low Pressure Conversion Temperature",
        "unit": "°C",
        "icon": "mdi:thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
    },
    "euv_powered_signal": {
        "dp_id": 101,
        "code": "euv_powered_signal",
        "raw_source": "status_parameter_group_1",
        "field_index": 18,
        "encoding": "int32_be",
        "name": "EUV Powered Signal",
        "icon": "mdi:signal",
    },
    "sg_grid_signal": {
        "dp_id": 101,
        "code": "sg_grid_signal",
        "raw_source": "status_parameter_group_1",
        "field_index": 19,
        "encoding": "int32_be",
        "name": "SG Grid Signal",
        "icon": "mdi:signal",
    },

    # ---- status_parameter_group_2 (dp 102) — totals & billing ----
    # NOTE: scaling values below are from @tomoo777's live app verification.
    "total_effluent_temperature": {
        "dp_id": 102,
        "code": "total_effluent_temperature",
        "raw_source": "status_parameter_group_2",
        "field_index": 0,
        "encoding": "int32_be",
        "conversion": "value / 10",   # verified: 239 → 23.9°C
        "name": "Total Effluent Temperature",
        "unit": "°C",
        "icon": "mdi:thermometer-water",
        "device_class": "temperature",
        "state_class": "measurement",
    },
    "heat_pump_billing_cost": {
        "dp_id": 102,
        "code": "heat_pump_billing_cost",
        "raw_source": "status_parameter_group_2",
        "field_index": 1,
        "encoding": "int32_be",
        "conversion": "value / 100",  # verified: 38 → 0.38
        "name": "Heat Pump Billing Cost",
        "icon": "mdi:currency-usd",
        "state_class": "measurement",
    },
    "gas_billing_cost": {
        "dp_id": 102,
        "code": "gas_billing_cost",
        "raw_source": "status_parameter_group_2",
        "field_index": 2,
        "encoding": "int32_be",
        "conversion": "value / 100",  # verified: 46 → 0.46
        "name": "Gas Billing Cost",
        "icon": "mdi:currency-usd",
        "state_class": "measurement",
    },

    # ---- parameter_group_23 (dp 140) — capacity, flow, power, energy ----
    "heating_cooling_capacity": {
        "dp_id": 140,
        "code": "heating_cooling_capacity",
        "raw_source": "parameter_group_23",
        "field_index": 0,
        "encoding": "int32_be",
        "conversion": "value / 10",   # verified: 47 → 4.7 kW
        "name": "Heating/Cooling Capacity",
        "unit": "kW",
        "icon": "mdi:heat-pump",
        "device_class": "power",
        "state_class": "measurement",
    },
    "water_flow_rate": {
        "dp_id": 140,
        "code": "water_flow_rate",
        "raw_source": "parameter_group_23",
        "field_index": 1,
        "encoding": "int32_be",
        "conversion": "value / 100",  # verified live
        "name": "Water Flow Rate",
        "unit": "m³/h",
        "icon": "mdi:water-pump",
        "state_class": "measurement",
    },
    "machine_power": {
        "dp_id": 140,
        "code": "machine_power",
        "raw_source": "parameter_group_23",
        "field_index": 4,
        "encoding": "int32_be",
        "name": "Machine Power",
        "unit": "W",
        "icon": "mdi:flash",
        "device_class": "power",
        "state_class": "measurement",
    },
    "cop_eer": {
        "dp_id": 140,
        "code": "cop_eer",
        "raw_source": "parameter_group_23",
        "field_index": 5,
        "encoding": "int32_be",
        "conversion": "value / 10",   # verified live
        "name": "COP / EER",
        "icon": "mdi:chart-line",
        "state_class": "measurement",
    },
    "daily_power_consumption": {
        "dp_id": 140,
        "code": "daily_power_consumption",
        "raw_source": "parameter_group_23",
        "field_index": 10,
        "encoding": "int32_be",
        "name": "Daily Power Consumption",
        "unit": "kWh",
        "icon": "mdi:chart-line",
        "device_class": "energy",
        # Device resets to 0 at midnight, so use total_increasing for
        # HA Energy dashboard compatibility.
        "state_class": "total_increasing",
    },

    # ---- Original non-raw sensors ----
    # Product ID (dp_id: 180)
    "products_id": {
        "dp_id": 180,
        "code": "products_id",
        "name": "Product ID",
        "icon": "mdi:identifier",
    },
    # Fault Code - Raw Bitmap Value (dp_id: 15)
    "fault_code": {
        "dp_id": 15,
        "code": "fault_code",
        "name": "Fault Code 1",
        "icon": "mdi:alert-circle",
        "device_class": "problem",
        "state_class": "measurement",
    },
    # Fault 2 - Raw Bitmap Value (dp_id: 198)
    "fault2_code": {
        "dp_id": 198,
        "code": "fault2_code",
        "name": "Fault Code 2",
        "icon": "mdi:alert-circle",
        "device_class": "problem",
        "state_class": "measurement",
    },
    # Custom Fault Bit (dp_id: 199)
    "custom_fault_bit": {
        "dp_id": 199,
        "code": "custom_fault_bit",
        "name": "Driver Fault (Er20)",
        "icon": "mdi:alert-circle",
        "device_class": "problem",
        "state_class": "measurement",
    },
}

# ====================================================
# BINARY SENSOR TYPES (read-only bitmap - accessMode: "ro")
# ====================================================
BINARY_SENSOR_TYPES = {
    # Fault Status (dp_id: 15)
    "fault": {
        "dp_id": 15,
        "code": "fault",
        "name": "Fault Status 1",
        "device_class": "problem",
        "conversion": "value != 0",
    },
    # Fault 2 Status (dp_id: 198)
    "fault2": {
        "dp_id": 198,
        "code": "fault2",
        "name": "Fault Status 2",
        "device_class": "problem",
        "conversion": "value != 0",
    },
}

# ====================================================
# SWITCH TYPES (read-write bool - accessMode: "rw")
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
    # Reset to Default (dp_id: 125) - accessMode: "wr"
    "reset": {
        "dp_id": 125,
        "code": "reset",
        "name": "Reset to Default",
        "icon": "mdi:restore",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']",
    },
}

# ====================================================
# NUMBER TYPES (read-write value - accessMode: "rw")
# ====================================================
NUMBER_TYPES = {
    # Hot Water Temperature Setpoint (dp_id: 110)
    "wth_set": {
        "dp_id": 110,
        "code": "wth_set",
        "name": "Hot Water Temperature",
        "icon": "mdi:water-thermometer",
        "unit": "°C",
        "min_value": 0.0,
        "max_value": 99.0,
        "step": 1.0,
        "api_conversion": "value",
    },
    # Heating Temperature Setpoint (dp_id: 111)
    "heating_set": {
        "dp_id": 111,
        "code": "heating_set",
        "name": "Heating Temperature",
        "icon": "mdi:thermostat",
        "unit": "°C",
        "min_value": 0.0,
        "max_value": 99.0,
        "step": 1.0,
        "api_conversion": "value",
    },
    # Cooling Temperature Setpoint (dp_id: 112)
    "cooling_set": {
        "dp_id": 112,
        "code": "cooling_set",
        "name": "Cooling Temperature",
        "icon": "mdi:snowflake",
        "unit": "°C",
        "min_value": 0.0,
        "max_value": 99.0,
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
