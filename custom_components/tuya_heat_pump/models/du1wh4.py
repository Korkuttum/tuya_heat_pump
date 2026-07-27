"""Model mapping for Alps Exclusive Heat Pump (du1wh4)."""

MODEL_NAME = "Alps Exclusive Heat Pump (du1wh4)"
# ====================================================
# Alps Exclusive @simonboerstra
#
# UPDATE 2026-07-27: parameter_group_1 (dp_id 118), parameter_group_2
# (dp_id 119) and parameter_group_23 (dp_id 140) have been decoded via
# raw_explorer.py — see the entries below. This device has NO plain
# adjustable target-temperature DP in the Standard set, but the
# setpoints turned out to live inside parameter_group_1:
# "heating_setting_temperature", "cooling_setting_temperature" and
# "hot_water_setting_temperature" are now exposed as number entities.
#
# parameter_group_3 through parameter_group_8 (dp_id 120-126, all
# 128-byte "raw" type blobs) are still SKIPPED / not decoded. If
# simonboerstra runs raw_explorer.py on these too, we can add
# individual fields from them later.
# ====================================================

SENSOR_TYPES = {
    # Fault Alarm (dp_id: 15) — bitmap, 30 possible faults. Tuya's own
    # catalog gave no descriptions (just bare Er-codes) — meanings
    # below provided by @simonboerstra from his unit's manual, and
    # independently confirmed against a real Er05 (High Pressure
    # Fault) occurrence on his own device.
    "fault": {
        "dp_id": 15,
        "code": "fault",
        "name": "Fault Alarm",
        "icon": "mdi:alert-circle",
        "conversion": (
            "', '.join(n for b, n in ["
            "(1,'Er03 - Water Flow Failure'),"
            "(2,'Er04 - Antifreeze Protection'),"
            "(4,'Er05 - High Pressure Fault'),"
            "(8,'Er06 - Low Pressure Fault'),"
            "(16,'Er09 - Communication Failure'),"
            "(32,'Er10 - Frequency Conversion Module Communication Failure'),"
            "(64,'Er12 - Exhaust Temperature Too High Protection'),"
            "(128,'Er14 - Water Tank Temperature Sensor Fault'),"
            "(256,'Er15 - Water Inlet Temperature Sensor Fault'),"
            "(512,'Er16 - Evaporator Coil Temperature Sensor Fault'),"
            "(1024,'Er18 - Exhaust Temperature Sensor Fault'),"
            "(2048,'Er20 - Frequency Conversion Module Abnormal Protection'),"
            "(4096,'Er21 - Ambient Temperature Sensor Fault'),"
            "(8192,'Er23 - Cooling Outlet Water Temperature Supercooling Protection'),"
            "(16384,'Er26 - Heat Sink Temperature Sensor Fault'),"
            "(32768,'Er27 - Outlet Water Temperature Sensor Fault'),"
            "(65536,'Er29 - Return Gas Temperature Sensor Fault'),"
            "(131072,'Er32 - Heating Outlet Water Temperature Too High Protection'),"
            "(262144,'Er33 - Coil Temperature Too High'),"
            "(524288,'Er34 - Frequency Conversion Module Temperature Too High'),"
            "(1048576,'Er42 - Cooling Coil Temperature Sensor Failure'),"
            "(2097152,'Er62 - Economizer Inlet Temperature Sensor Fault'),"
            "(4194304,'Er63 - Economizer Outlet Temperature Sensor Fault'),"
            "(8388608,'Er64 - DC Fan 1 Fault'),"
            "(16777216,'Er66 - DC Fan 2 Fault'),"
            "(33554432,'Er67 - Low Pressure Switch Failure'),"
            "(67108864,'Er68 - High Pressure Switch Failure'),"
            "(134217728,'Er69 - Low Pressure Protection'),"
            "(268435456,'Er70 - High Pressure Protection'),"
            "(536870912,'Er73 - Compressor Discharge Overcurrent Protection')"
            "] if value & b) or 'OK'"
        ),
    },
    "intemp": {
        "dp_id": 101,
        "code": "intemp",
        "name": "Water Inlet Temperature",
        "unit": "°C",
        "icon": "mdi:thermometer-water",
        "device_class": "temperature",
        "state_class": "measurement",
    },
    "outtemp": {
        "dp_id": 102,
        "code": "outtemp",
        "name": "Water Outlet Temperature",
        "unit": "°C",
        "icon": "mdi:thermometer-water",
        "device_class": "temperature",
        "state_class": "measurement",
    },
    "whjtemp": {
        "dp_id": 103,
        "code": "whjtemp",
        "name": "Ambient Temperature",
        "unit": "°C",
        "icon": "mdi:home-thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
    },
    "cmptemp": {
        "dp_id": 104,
        "code": "cmptemp",
        "name": "Discharge Temperature",
        "unit": "°C",
        "icon": "mdi:thermometer-alert",
        "device_class": "temperature",
        "state_class": "measurement",
    },
    "hqtemp": {
        "dp_id": 105,
        "code": "hqtemp",
        "name": "Return Gas Temperature",
        "unit": "°C",
        "icon": "mdi:thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
    },
    "ptemp": {
        "dp_id": 106,
        "code": "ptemp",
        "name": "Outdoor Coil Temperature",
        "unit": "°C",
        "icon": "mdi:thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
    },
    "cptemp": {
        "dp_id": 107,
        "code": "cptemp",
        "name": "Cooling Coil Temperature",
        "unit": "°C",
        "icon": "mdi:thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
    },
    "wttemp": {
        "dp_id": 108,
        "code": "wttemp",
        "name": "Water Tank Temperature",
        "unit": "°C",
        "icon": "mdi:thermometer-water",
        "device_class": "temperature",
        "state_class": "measurement",
    },
    "step_run": {
        "dp_id": 109,
        "code": "step_run",
        "name": "Main Valve Opening",
        "unit": "P",
        "icon": "mdi:valve",
    },
    "stepb_run": {
        "dp_id": 111,
        "code": "stepb_run",
        "name": "EVI Valve Opening",
        "unit": "P",
        "icon": "mdi:valve",
    },
    "cmp_cur": {
        "dp_id": 112,
        "code": "cmp_cur",
        "name": "Compressor Current",
        "unit": "A",
        "icon": "mdi:current-ac",
        "device_class": "current",
        "state_class": "measurement",
    },
    "sink_temp": {
        "dp_id": 113,
        "code": "sink_temp",
        "name": "Heatsink Temperature",
        "unit": "°C",
        "icon": "mdi:thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
    },
    "dc_bus_voltage": {
        "dp_id": 114,
        "code": "dc_bus_voltage",
        "name": "DC Bus Voltage",
        "unit": "V",
        "icon": "mdi:flash",
        "device_class": "voltage",
        "state_class": "measurement",
    },
    "cmp_act_frep": {
        "dp_id": 115,
        "code": "cmp_act_frep",
        "name": "Compressor Frequency",
        "unit": "Hz",
        "icon": "mdi:sine-wave",
        "state_class": "measurement",
    },
    "dc_fan_speed": {
        "dp_id": 116,
        "code": "dc_fan_speed",
        "name": "DC Fan 1 Speed",
        "unit": "rpm",
        "icon": "mdi:fan",
        "state_class": "measurement",
    },
    "dc_fan2_speed": {
        "dp_id": 117,
        "code": "dc_fan2_speed",
        "name": "DC Fan 2 Speed",
        "unit": "rpm",
        "icon": "mdi:fan",
        "state_class": "measurement",
    },
}

# ====================================================
# BINARY SENSOR TYPES (read-only bitmap - accessMode: "ro")
# ====================================================
BINARY_SENSOR_TYPES = {
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
    "switch": {
        "dp_id": 1,
        "code": "switch",
        "name": "Power",
        "icon": "mdi:power",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']",
    },
    # accessMode is "wr" (not the usual "rw") in Tuya's own schema —
    # a write-triggered action, only takes effect while the unit is
    # powered off (per Tuya's own description text for this DP).
    "reset": {
        "dp_id": 125,
        "code": "reset",
        "name": "Factory Reset",
        "icon": "mdi:restore",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']",
    },
    # --- decoded from parameter_group_1 / parameter_group_2 via raw_explorer.py (2026-07-27) ---
    "heating_target_temperature_automatic_adjustment_enable": {
        "dp_id": 118,
        "code": "heating_target_temperature_automatic_adjustment_enable",
        "raw_source": "parameter_group_1",
        "field_index": 11,
        "encoding": "int32_be",
        "name": "Heating Target Temperature Automatic Adjustment Enable",
        "icon": "mdi:thermostat-auto",
    },
    "frequency_operating_mode_after_constant_temperature": {
        "dp_id": 118,
        "code": "frequency_operating_mode_after_constant_temperature",
        "raw_source": "parameter_group_1",
        "field_index": 14,
        "encoding": "int32_be",
        "name": "Frequency Operating Mode After Constant Temperature",
        "icon": "mdi:sine-wave",
    },
    "heat_pump_fuction": {
        "dp_id": 118,
        "code": "heat_pump_fuction",
        "raw_source": "parameter_group_1",
        "field_index": 17,
        "encoding": "int32_be",
        "name": "Heat Pump Function",
        "icon": "mdi:heat-pump",
    },
    "circulation_pump_status_after_reaching_target_temp": {
        "dp_id": 118,
        "code": "circulation_pump_status_after_reaching_target_temp",
        "raw_source": "parameter_group_1",
        "field_index": 18,
        "encoding": "int32_be",
        "name": "Circulation Pump Status After Reaching Target Temp",
        "icon": "mdi:pump",
    },
    "dc_circulation_pump_mode": {
        "dp_id": 119,
        "code": "dc_circulation_pump_mode",
        "raw_source": "parameter_group_2",
        "field_index": 0,
        "encoding": "int32_be",
        "name": "DC Circulation Pump Mode",
        "icon": "mdi:pump",
    },
}

# ====================================================
# NUMBER TYPES (read-write value - accessMode: "rw")
# ====================================================
# All entries below decoded from parameter_group_1 (dp_id 118),
# parameter_group_2 (dp_id 119) and parameter_group_23 (dp_id 140)
# via raw_explorer.py (2026-07-27). This is where the target
# temperature setpoints turned out to live — see the note at the
# top of this file.
NUMBER_TYPES = {
    "temp_difference_of_return_water_and_coolingheating_target_temp": {
        "dp_id": 118,
        "code": "temp_difference_of_return_water_and_coolingheating_target_temp",
        "raw_source": "parameter_group_1",
        "field_index": 0,
        "encoding": "int32_be",
        "min_value": 2,
        "max_value": 18,
        "step": 1,
        "name": "Temp Difference of Return Water and Cooling/Heating Target Temp",
        "unit": "°C",
        "icon": "mdi:thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
    },
    "temp_difference_of_return_water_and_hot_water_target_temp": {
        "dp_id": 118,
        "code": "temp_difference_of_return_water_and_hot_water_target_temp",
        "raw_source": "parameter_group_1",
        "field_index": 1,
        "encoding": "int32_be",
        "min_value": 2,
        "max_value": 18,
        "step": 1,
        "name": "Temp Difference of Return Water and Hot Water Target Temp",
        "unit": "°C",
        "icon": "mdi:thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
    },
    # --- Target temperature setpoints (previously missing from the Standard DP set) ---
    "hot_water_setting_temperature": {
        "dp_id": 118,
        "code": "hot_water_setting_temperature",
        "raw_source": "parameter_group_1",
        "field_index": 2,
        "encoding": "int32_be",
        "min_value": 28,
        "max_value": 70,
        "step": 1,
        "name": "Hot Water Setting Temperature",
        "unit": "°C",
        "icon": "mdi:thermometer-water",
        "device_class": "temperature",
        "state_class": "measurement",
    },
    "cooling_setting_temperature": {
        "dp_id": 118,
        "code": "cooling_setting_temperature",
        "raw_source": "parameter_group_1",
        "field_index": 3,
        "encoding": "int32_be",
        "min_value": 12,
        "max_value": 30,
        "step": 1,
        "name": "Cooling Setting Temperature",
        "unit": "°C",
        "icon": "mdi:snowflake-thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
    },
    "heating_setting_temperature": {
        "dp_id": 118,
        "code": "heating_setting_temperature",
        "raw_source": "parameter_group_1",
        "field_index": 4,
        "encoding": "int32_be",
        "min_value": 15,
        "max_value": 70,
        "step": 1,
        "name": "Heating Setting Temperature",
        "unit": "°C",
        "icon": "mdi:thermometer-lines",
        "device_class": "temperature",
        "state_class": "measurement",
    },
    "high_temperature_desinfection_cycle_days": {
        "dp_id": 118,
        "code": "high_temperature_desinfection_cycle_days",
        "raw_source": "parameter_group_1",
        "field_index": 6,
        "encoding": "int32_be",
        "step": 1,
        "name": "High Temperature Desinfection Cycle Days",
        "icon": "mdi:calendar-sync",
    },
    "high_temperature_desinfection_start_time": {
        "dp_id": 118,
        "code": "high_temperature_desinfection_start_time",
        "raw_source": "parameter_group_1",
        "field_index": 7,
        "encoding": "int32_be",
        "step": 1,
        "name": "High Temperature Desinfection Start Time",
        "icon": "mdi:clock-start",
    },
    "high_temperature_desinfection_sustaining_time": {
        "dp_id": 118,
        "code": "high_temperature_desinfection_sustaining_time",
        "raw_source": "parameter_group_1",
        "field_index": 8,
        "encoding": "int32_be",
        "step": 1,
        "name": "High Temperature Desinfection Sustaining Time",
        "icon": "mdi:clock-outline",
    },
    "high_temperature_desinfection_setting_temperature": {
        "dp_id": 118,
        "code": "high_temperature_desinfection_setting_temperature",
        "raw_source": "parameter_group_1",
        "field_index": 9,
        "encoding": "int32_be",
        "step": 1,
        "name": "High Temperature Desinfection Setting Temperature",
        "unit": "°C",
        "icon": "mdi:thermometer-high",
        "device_class": "temperature",
        "state_class": "measurement",
    },
    "heat_pumps_setting_temperature_for_high_temperature_desinfection": {
        "dp_id": 118,
        "code": "heat_pumps_setting_temperature_for_high_temperature_desinfection",
        "raw_source": "parameter_group_1",
        "field_index": 10,
        "encoding": "int32_be",
        "step": 1,
        "name": "Heat Pump's Setting Temperature for High Temperature Desinfection",
        "unit": "°C",
        "icon": "mdi:thermometer-high",
        "device_class": "temperature",
        "state_class": "measurement",
    },
    "heating_compensation_temperature_point_ambient_temperature": {
        "dp_id": 118,
        "code": "heating_compensation_temperature_point_ambient_temperature",
        "raw_source": "parameter_group_1",
        "field_index": 12,
        "encoding": "int32_be",
        "min_value": 0,
        "max_value": 40,
        "step": 1,
        "name": "Heating Compensation Temperature Point (Ambient Temperature)",
        "unit": "°C",
        "icon": "mdi:thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
    },
    "target_temperature_compensation_coefficient": {
        "dp_id": 118,
        "code": "target_temperature_compensation_coefficient",
        "raw_source": "parameter_group_1",
        "field_index": 13,
        "encoding": "int32_be",
        "min_value": 0,
        "max_value": 30,
        "step": 1,
        "name": "Target Temperature Compensation Coefficient",
        "icon": "mdi:tune",
    },
    "ambient_temperature_for_starting_electric_heating": {
        "dp_id": 118,
        "code": "ambient_temperature_for_starting_electric_heating",
        "raw_source": "parameter_group_1",
        "field_index": 15,
        "encoding": "int32_be",
        "step": 1,
        "name": "Ambient Temperature for Starting Electric Heating",
        "unit": "°C",
        "icon": "mdi:thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
    },
    "start_time_for_electric_heating_of_water_tank": {
        "dp_id": 118,
        "code": "start_time_for_electric_heating_of_water_tank",
        "raw_source": "parameter_group_1",
        "field_index": 16,
        "encoding": "int32_be",
        "step": 1,
        "name": "Start Time for Electric Heating of Water Tank",
        "icon": "mdi:clock-start",
    },
    "circulation_pump_onoff_cycle_after_reaching_target_temp": {
        "dp_id": 118,
        "code": "circulation_pump_onoff_cycle_after_reaching_target_temp",
        "raw_source": "parameter_group_1",
        "field_index": 19,
        "encoding": "int32_be",
        "min_value": 0,
        "max_value": 120,
        "step": 1,
        "name": "Circulation Pump On-Off Cycle After Reaching Target Temp",
        "icon": "mdi:pump",
    },
    "dc_water_pump_manual_speed": {
        "dp_id": 119,
        "code": "dc_water_pump_manual_speed",
        "raw_source": "parameter_group_2",
        "field_index": 1,
        "encoding": "int32_be",
        "min_value": 0,
        "max_value": 100,
        "step": 1,
        "name": "DC Water Pump Manual Speed",
        "unit": "%",
        "icon": "mdi:pump",
    },
    "defrosting_frequency": {
        "dp_id": 119,
        "code": "defrosting_frequency",
        "raw_source": "parameter_group_2",
        "field_index": 2,
        "encoding": "int32_be",
        "min_value": 30,
        "max_value": 120,
        "step": 1,
        "name": "Defrosting Frequency",
        "unit": "Hz",
        "icon": "mdi:sine-wave",
        "device_class": "frequency",
        "state_class": "measurement",
    },
    "defrosting_period": {
        "dp_id": 119,
        "code": "defrosting_period",
        "raw_source": "parameter_group_2",
        "field_index": 3,
        "encoding": "int32_be",
        "min_value": 20,
        "max_value": 90,
        "step": 1,
        "name": "Defrosting Period",
        "icon": "mdi:snowflake-melt",
    },
    "defrost_enter_temp": {
        "dp_id": 119,
        "code": "defrost_enter_temp",
        "raw_source": "parameter_group_2",
        "field_index": 4,
        "encoding": "int32_be",
        "min_value": -15,
        "max_value": -1,
        "step": 1,
        "name": "Defrost Enter Temp",
        "unit": "°C",
        "icon": "mdi:snowflake-thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
    },
    "defrosting_time": {
        "dp_id": 119,
        "code": "defrosting_time",
        "raw_source": "parameter_group_2",
        "field_index": 5,
        "encoding": "int32_be",
        "min_value": 5,
        "max_value": 20,
        "step": 1,
        "name": "Defrosting Time",
        "icon": "mdi:snowflake-melt",
    },
    "defrost_exit_temp": {
        "dp_id": 119,
        "code": "defrost_exit_temp",
        "raw_source": "parameter_group_2",
        "field_index": 6,
        "encoding": "int32_be",
        "min_value": 1,
        "max_value": 40,
        "step": 1,
        "name": "Defrost Exit Temp",
        "unit": "°C",
        "icon": "mdi:thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
    },
    "defrosting_environment_and_evaporator_coil_temp_difference_1": {
        "dp_id": 119,
        "code": "defrosting_environment_and_evaporator_coil_temp_difference_1",
        "raw_source": "parameter_group_2",
        "field_index": 7,
        "encoding": "int32_be",
        "min_value": 0,
        "max_value": 15,
        "step": 1,
        "name": "Defrosting Environment and Evaporator Coil Temp Difference 1",
        "unit": "°C",
        "icon": "mdi:thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
    },
    "defrosting_environment_and_evaporator_coil_temp_difference_2": {
        "dp_id": 119,
        "code": "defrosting_environment_and_evaporator_coil_temp_difference_2",
        "raw_source": "parameter_group_2",
        "field_index": 8,
        "encoding": "int32_be",
        "min_value": 0,
        "max_value": 15,
        "step": 1,
        "name": "Defrosting Environment and Evaporator Coil Temp Difference 2",
        "unit": "°C",
        "icon": "mdi:thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
    },
    "ambient_temp_for_defrosting": {
        "dp_id": 119,
        "code": "ambient_temp_for_defrosting",
        "raw_source": "parameter_group_2",
        "field_index": 9,
        "encoding": "int32_be",
        "min_value": 0,
        "max_value": 20,
        "step": 1,
        "name": "Ambient Temp for Defrosting",
        "unit": "°C",
        "icon": "mdi:thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
    },
    "heating_capacitycooling_capacity": {
        "dp_id": 140,
        "code": "heating_capacitycooling_capacity",
        "raw_source": "parameter_group_23",
        "field_index": 0,
        "encoding": "int32_be",
        "conversion": "value / 10",
        "api_conversion": "value * 10",
        "step": 1,
        "name": "Heating Capacity / Cooling Capacity",
        "unit": "kW",
        "icon": "mdi:flash",
        "device_class": "power",
        "state_class": "measurement",
    },
    "current_water_flow_rate": {
        "dp_id": 140,
        "code": "current_water_flow_rate",
        "raw_source": "parameter_group_23",
        "field_index": 1,
        "encoding": "int32_be",
        "conversion": "value / 100",
        "api_conversion": "value * 100",
        "step": 1,
        "name": "Current Water Flow Rate",
        "unit": "m3/h",
        "icon": "mdi:water-pump",
    },
    "current_of_the_entire_machine": {
        "dp_id": 140,
        "code": "current_of_the_entire_machine",
        "raw_source": "parameter_group_23",
        "field_index": 2,
        "encoding": "int32_be",
        "conversion": "value / 10",
        "api_conversion": "value * 10",
        "step": 1,
        "name": "Current of the Entire Machine",
        "unit": "A",
        "icon": "mdi:current-ac",
        "device_class": "current",
        "state_class": "measurement",
    },
    "voltage_of_entire_machine": {
        "dp_id": 140,
        "code": "voltage_of_entire_machine",
        "raw_source": "parameter_group_23",
        "field_index": 3,
        "encoding": "int32_be",
        "step": 1,
        "name": "Voltage of Entire Machine",
        "unit": "V",
        "icon": "mdi:lightning-bolt",
        "device_class": "voltage",
        "state_class": "measurement",
    },
    "power_of_entire_machine": {
        "dp_id": 140,
        "code": "power_of_entire_machine",
        "raw_source": "parameter_group_23",
        "field_index": 4,
        "encoding": "int32_be",
        "step": 1,
        "name": "Power of Entire Machine",
        "unit": "W",
        "icon": "mdi:flash",
        "device_class": "power",
        "state_class": "measurement",
    },
    "copeer": {
        "dp_id": 140,
        "code": "copeer",
        "raw_source": "parameter_group_23",
        "field_index": 5,
        "encoding": "int32_be",
        "step": 1,
        "name": "COP (EER)",
        "icon": "mdi:gauge",
    },
    "current_year": {
        "dp_id": 140,
        "code": "current_year",
        "raw_source": "parameter_group_23",
        "field_index": 11,
        "encoding": "int32_be",
        "step": 1,
        "name": "Current Year",
        "icon": "mdi:calendar",
    },
    "current_month": {
        "dp_id": 140,
        "code": "current_month",
        "raw_source": "parameter_group_23",
        "field_index": 12,
        "encoding": "int32_be",
        "step": 1,
        "name": "Current Month",
        "icon": "mdi:calendar-month",
    },
    "current_day": {
        "dp_id": 140,
        "code": "current_day",
        "raw_source": "parameter_group_23",
        "field_index": 13,
        "encoding": "int32_be",
        "step": 1,
        "name": "Current Day",
        "icon": "mdi:calendar-today",
    },
}

# ====================================================
# SELECT TYPES (read-write enum - accessMode: "rw")
# ====================================================
SELECT_TYPES = {
    "mode": {
        "dp_id": 2,
        "code": "mode",
        "name": "Operating Mode",
        "icon": "mdi:hvac",
        "options": {
            "smart": "Smart",
            "strong": "Strong",
            "mute": "Mute",
        },
    },
    "work_mode": {
        "dp_id": 5,
        "code": "work_mode",
        "name": "Working Mode",
        "icon": "mdi:cog",
        "options": {
            "wth": "Hot Water",
            "heat": "Heating",
            "cool": "Cooling",
            "wth_heat": "Hot Water + Heating",
            "wth_cool": "Hot Water + Cooling",
        },
    },
    "temp_unit_convert": {
        "dp_id": 6,
        "code": "temp_unit_convert",
        "name": "Temperature Unit",
        "icon": "mdi:temperature-celsius",
        "options": {
            "c": "Celsius",
            "f": "Fahrenheit",
        },
    },
}
