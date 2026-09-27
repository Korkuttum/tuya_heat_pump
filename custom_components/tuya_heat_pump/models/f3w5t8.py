"""Model mapping for Alps Exclusive Heat Pump (f3w5t8)."""

MODEL_NAME = "Alps Exclusive Heat Pump (f3w5t8)"
# ====================================================
# Alps Exclusive (f3w5t8 variant) @jorisijji, issue #70
# ====================================================
# This is a DIFFERENT Tuya modelId from the Alps Exclusive already
# supported (du1wh4) — same brand, different internal hardware batch.
# With no model file of its own it was falling back to default.py,
# whose DP codes don't match this device at all, hence most entities
# showing unavailable.
#
# DP layout (switch/mode/work_mode/temp_unit_convert/wth_set/
# heating_set/cooling_set/status_parameter_group_1-2/
# parameter_group_1-10/reset/hdef/parameter_group_23/products_id/
# fault2/custom_fault_bit) is identical to the "Power World OEM" family
# (e1k5wjuc, e1nde5gc) — same dp_ids, same codes — so the plain DPs
# below are taken directly from this device's own typeSpec, matching
# that family's proven entity design.
#
# UNRESOLVED — raw parameter groups: status_parameter_group_1/2 (dp
# 101/102, likely live telemetry), parameter_group_1-10 (dp 118-124,
# 126-128, config) and parameter_group_23 (dp 140, "electricity
# statistics") have no field-level breakdown for this specific device —
# run test/raw_explorer.py to map them (same process as issue #53).
#
# fault (dp 15): 25 of this device's 30 codes match @simonboerstra's
# confirmed Alps translations (du1wh4, this same issue) one-for-one, so
# those are reused directly. The remaining 5 (Er72, Er74, Er75, Er76,
# Er01) don't appear in that list — shown as bare codes until someone
# provides their meaning.
#
# wth_set/heating_set/cooling_set: @tomoo777 found (issue #53, same OEM
# family) that e1k5wjuc silently multiplies whatever raw value it's
# written by 10 to get its real target temperature. This device's
# typeSpec is otherwise identical, so the same quirk is plausible here
# too — but NOT yet confirmed for this specific device, so left
# unscaled (api_conversion "value") rather than guessed. To check:
# type a value into one of these in HA, then look at the same setpoint
# in the Smart Life app — if the app shows 10× what you typed, apply
# the same "value / 10" fix used in e1k5wjuc.py.

SENSOR_TYPES = {
    # Fault Description (dp_id: 15) — see header note on translation
    # coverage.
    "fault": {
        "dp_id": 15,
        "code": "fault",
        "name": "Fault Description",
        "icon": "mdi:alert-circle",
        "conversion": (
            "', '.join(n for b, n in ["
            "(1,'Er03: Water flow failure'),"
            "(2,'Er73: Compressor discharge overcurrent protection'),"
            "(4,'Er05: High pressure fault'),"
            "(8,'Er06: Low pressure fault'),"
            "(16,'Er09: Communication failure'),"
            "(32,'Er10: Frequency conversion module communication failure'),"
            "(64,'Er12: Exhaust temperature too high protection'),"
            "(128,'Er14: Water tank temperature sensor fault'),"
            "(256,'Er15: Water inlet temperature sensor fault'),"
            "(512,'Er16: Evaporator coil temperature sensor fault'),"
            "(1024,'Er18: Exhaust temperature sensor fault'),"
            "(2048,'Er20: Frequency conversion module abnormal protection'),"
            "(4096,'Er21: Ambient temperature sensor fault'),"
            "(8192,'Er23: Cooling outlet water temperature supercooling protection'),"
            "(16384,'Er72'),"
            "(32768,'Er27: Outlet water temperature sensor fault'),"
            "(65536,'Er29: Return gas temperature sensor fault'),"
            "(131072,'Er32: Heating outlet water temperature too high protection'),"
            "(262144,'Er33: Coil temperature too high'),"
            "(524288,'Er74'),"
            "(1048576,'Er42: Cooling coil temperature sensor failure'),"
            "(2097152,'Er75'),"
            "(4194304,'Er76'),"
            "(8388608,'Er64: DC Fan 1 fault'),"
            "(16777216,'Er66: DC Fan 2 fault'),"
            "(33554432,'Er67: Low pressure switch failure'),"
            "(67108864,'Er68: High pressure switch failure'),"
            "(134217728,'Er69: Low pressure protection'),"
            "(268435456,'Er70: High pressure protection'),"
            "(536870912,'Er01')"
            "] if value & b) or 'OK'"
        ),
    },
    # Extra Fault Description (dp_id: 198) — DC water pump fault group.
    "fault2": {
        "dp_id": 198,
        "code": "fault2",
        "name": "Extra Fault Description",
        "icon": "mdi:alert-circle-outline",
        "conversion": (
            "', '.join(n for b, n in ["
            "(1,'Er79: DC Water Pump Undervoltage Fault'),"
            "(2,'Er80: DC Water Pump Stall/Locked-Rotor Fault'),"
            "(4,'Er81: DC Water Pump Other Fault'),"
            "(8,'Er82: DC Water Pump Communication Fault')"
            "] if value & b) or 'OK'"
        ),
    },
    # Custom Fault Bit (dp_id: 199) — inverter drive Er20 fault register,
    # per Tuya's own (untranslated) name for this DP.
    "custom_fault_bit": {
        "dp_id": 199,
        "code": "custom_fault_bit",
        "name": "Inverter Drive Fault Code",
        "icon": "mdi:alert-circle",
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
    "fault": {
        "dp_id": 15,
        "code": "fault",
        "name": "Fault Status",
        "device_class": "problem",
        "conversion": "value != 0",
    },
    "fault2": {
        "dp_id": 198,
        "code": "fault2",
        "name": "Extra Fault Status",
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
    # See header note — write scaling unconfirmed for this device.
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
# ====================================================
# Raw parameter groups @jorisijji (via raw_explorer.py) + PR #92
# (@Rolf2211) for the OEM-family-confirmed dp102/dp140 scaling
# ====================================================
# Fills in the "UNRESOLVED" raw groups noted in the header above.
# status_parameter_group_1/2 (dp 101/102) are read-only live telemetry;
# parameter_group_1/2/8/9 (dp 118/119/126/127) are genuine writable
# settings; parameter_group_23 (dp 140, "electricity statistics") mixes
# a few live measurements in among writable fields.
#
# dp101 field labels/units below are @Rolf2211's from PR #92, which
# match this device's own DP layout field-for-field with @jorisijji's
# independent raw_explorer.py export (same OEM family, same offsets) --
# used here since they're already in English.
#
# dp102 and dp140's scaling (the /10, /100 conversions, and the two
# billing-cost + daily-power fields PR #92 adds that weren't in
# @jorisijji's export) come from PR #92, which reuses @tomoo777's
# live-confirmed values for this exact same OEM family from issue #53
# (e1k5wjuc) rather than guessing -- e.g. total_effluent_temperature
# confirmed there as 239 -> 23.9 °C. PR #92's extra "fault_code"/
# "fault2_code" entries for dp 15/198 were left out -- this file
# already has properly translated fault descriptions for both.
#
# Two fields (DC circulation pump mode, circulation pump status after
# reaching setpoint) are left as plain numbers rather than selects --
# @simonboerstra's manual gave named options for these on the OTHER
# Alps model (du1wh4), but that's a different physical unit and the
# options aren't confirmed for this one yet.

# --- merge into SENSOR_TYPES (status_parameter_group_1/2 + parameter_group_23 telemetry) ---
SENSOR_TYPES = globals().get("SENSOR_TYPES", {})
SENSOR_TYPES.update({
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
        "icon": "mdi:thermometer",
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
        "icon": "mdi:thermometer",
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
        "icon": "mdi:thermometer",
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
        "icon": "mdi:thermometer",
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
        "icon": "mdi:valve",
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
        "icon": "mdi:valve",
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
        "icon": "mdi:flash",
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
        "icon": "mdi:sine-wave",
        "device_class": "frequency",
        "state_class": "measurement",
    },
    # Original raw_explorer.py export had two fan fields both pointing at
    # field_index 15 (a copy/paste slip) -- corrected here to 14/15 so
    # each fan gets its own reading instead of one silently overwriting
    # the other.
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
        "state_class": "measurement",
    },
    "sg_grid_signal": {
        "dp_id": 101,
        "code": "sg_grid_signal",
        "raw_source": "status_parameter_group_1",
        "field_index": 19,
        "encoding": "int32_be",
        "name": "SG Grid Signal",
        "icon": "mdi:signal",
        "state_class": "measurement",
    },
    # status_parameter_group_2 (dp 102) -- scaling confirmed for this
    # OEM family in issue #53 (e1k5wjuc): 239 -> 23.9 °C, 38 -> 0.38, 46 -> 0.46.
    "total_effluent_temperature": {
        "dp_id": 102,
        "code": "total_effluent_temperature",
        "raw_source": "status_parameter_group_2",
        "field_index": 0,
        "encoding": "int32_be",
        "conversion": "value / 10",
        "name": "Total Effluent Temperature",
        "unit": "°C",
        "icon": "mdi:thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
    },
    "heat_pump_billing_cost": {
        "dp_id": 102,
        "code": "heat_pump_billing_cost",
        "raw_source": "status_parameter_group_2",
        "field_index": 1,
        "encoding": "int32_be",
        "conversion": "value / 100",
        "name": "Heat Pump Billing Cost",
        "icon": "mdi:cash",
        "state_class": "measurement",
    },
    "gas_billing_cost": {
        "dp_id": 102,
        "code": "gas_billing_cost",
        "raw_source": "status_parameter_group_2",
        "field_index": 2,
        "encoding": "int32_be",
        "conversion": "value / 100",
        "name": "Gas Billing Cost",
        "icon": "mdi:cash",
        "state_class": "measurement",
    },
    # Live metrics living inside parameter_group_23 (dp 140) -- read-only
    # even though most of that DP's other fields are real settings.
    # Scaling confirmed for this OEM family in issue #53 (e1k5wjuc).
    "heating_cooling_capacity": {
        "dp_id": 140,
        "code": "heating_cooling_capacity",
        "raw_source": "parameter_group_23",
        "field_index": 0,
        "encoding": "int32_be",
        "conversion": "value / 10",
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
        "conversion": "value / 100",
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
        "conversion": "value / 10",
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
        "state_class": "total_increasing",
    },
    "year": {
        "dp_id": 140,
        "code": "year",
        "raw_source": "parameter_group_23",
        "field_index": 11,
        "encoding": "int32_be",
        "name": "Year",
        "icon": "mdi:calendar",
    },
    "month": {
        "dp_id": 140,
        "code": "month",
        "raw_source": "parameter_group_23",
        "field_index": 12,
        "encoding": "int32_be",
        "name": "Month",
        "icon": "mdi:calendar",
    },
    "day": {
        "dp_id": 140,
        "code": "day",
        "raw_source": "parameter_group_23",
        "field_index": 13,
        "encoding": "int32_be",
        "name": "Day",
        "icon": "mdi:calendar",
    },
    "hour": {
        "dp_id": 140,
        "code": "hour",
        "raw_source": "parameter_group_23",
        "field_index": 14,
        "encoding": "int32_be",
        "name": "Hour",
        "icon": "mdi:clock-outline",
    },
    "minute": {
        "dp_id": 140,
        "code": "minute",
        "raw_source": "parameter_group_23",
        "field_index": 15,
        "encoding": "int32_be",
        "name": "Minute",
        "icon": "mdi:clock-outline",
    },
    "second": {
        "dp_id": 140,
        "code": "second",
        "raw_source": "parameter_group_23",
        "field_index": 16,
        "encoding": "int32_be",
        "name": "Second",
        "icon": "mdi:clock-outline",
    },
})

# --- merge into NUMBER_TYPES (genuine settings, from @jorisijji's export) ---
NUMBER_TYPES = globals().get("NUMBER_TYPES", {})
NUMBER_TYPES.update({
    "temp_diff_return_water_cooling": {
        "dp_id": 118,
        "code": "temp_diff_return_water_cooling",
        "raw_source": "parameter_group_1",
        "field_index": 0,
        "encoding": "int32_be",
        "step": 1,
        "name": "Temp. Diff: Return Water vs Cooling Temp",
        "unit": "°C",
        "icon": "mdi:thermometer",
        "device_class": "temperature",
    },
    "temp_diff_return_water_hot_water": {
        "dp_id": 118,
        "code": "temp_diff_return_water_hot_water",
        "raw_source": "parameter_group_1",
        "field_index": 1,
        "encoding": "int32_be",
        "step": 1,
        "name": "Temp. Diff: Return Water vs Hot Water Temp",
        "unit": "°C",
        "icon": "mdi:thermometer",
        "device_class": "temperature",
    },
    "hot_water_setpoint": {
        "dp_id": 118,
        "code": "hot_water_setpoint",
        "raw_source": "parameter_group_1",
        "field_index": 2,
        "encoding": "int32_be",
        "step": 1,
        "name": "Hot Water Setpoint",
        "unit": "°C",
        "icon": "mdi:thermometer",
        "device_class": "temperature",
    },
    "cooling_setpoint": {
        "dp_id": 118,
        "code": "cooling_setpoint",
        "raw_source": "parameter_group_1",
        "field_index": 3,
        "encoding": "int32_be",
        "step": 1,
        "name": "Cooling Setpoint",
        "unit": "°C",
        "icon": "mdi:snowflake",
        "device_class": "temperature",
    },
    "heating_setpoint": {
        "dp_id": 118,
        "code": "heating_setpoint",
        "raw_source": "parameter_group_1",
        "field_index": 4,
        "encoding": "int32_be",
        "step": 1,
        "name": "Heating Setpoint",
        "unit": "°C",
        "icon": "mdi:thermostat",
        "device_class": "temperature",
    },
    "disinfection_start_time_high_temp": {
        "dp_id": 118,
        "code": "disinfection_start_time_high_temp",
        "raw_source": "parameter_group_1",
        "field_index": 7,
        "encoding": "int32_be",
        "step": 1,
        "name": "Disinfection Start Time (High Temp)",
    },
    "disinfection_duration_high_temp": {
        "dp_id": 118,
        "code": "disinfection_duration_high_temp",
        "raw_source": "parameter_group_1",
        "field_index": 8,
        "encoding": "int32_be",
        "step": 1,
        "name": "Disinfection Duration (High Temp)",
    },
    "legionella_setpoint_temperature": {
        "dp_id": 118,
        "code": "legionella_setpoint_temperature",
        "raw_source": "parameter_group_1",
        "field_index": 9,
        "encoding": "int32_be",
        "step": 1,
        "name": "Legionella Setpoint Temperature",
        "unit": "°C",
        "icon": "mdi:thermometer",
        "device_class": "temperature",
    },
    "high_temp_disinfection_setpoint": {
        "dp_id": 118,
        "code": "high_temp_disinfection_setpoint",
        "raw_source": "parameter_group_1",
        "field_index": 10,
        "encoding": "int32_be",
        "step": 1,
        "name": "High-Temp Disinfection Setpoint",
        "unit": "°C",
        "icon": "mdi:thermometer",
        "device_class": "temperature",
    },
    "heating_compensation_ambient_temp_point": {
        "dp_id": 118,
        "code": "heating_compensation_ambient_temp_point",
        "raw_source": "parameter_group_1",
        "field_index": 12,
        "encoding": "int32_be",
        "step": 1,
        "name": "Heating Compensation Ambient Temp Point",
        "unit": "°C",
        "icon": "mdi:thermometer",
        "device_class": "temperature",
    },
    "target_temperature_compensation_factor": {
        "dp_id": 118,
        "code": "target_temperature_compensation_factor",
        "raw_source": "parameter_group_1",
        "field_index": 13,
        "encoding": "int32_be",
        "step": 1,
        "name": "Target Temperature Compensation Factor",
    },
    "electric_heating_ambient_temp_threshold": {
        "dp_id": 118,
        "code": "electric_heating_ambient_temp_threshold",
        "raw_source": "parameter_group_1",
        "field_index": 15,
        "encoding": "int32_be",
        "step": 1,
        "name": "Electric Heating Ambient Temp Threshold",
        "unit": "°C",
        "icon": "mdi:thermometer",
        "device_class": "temperature",
    },
    "tank_electric_heating_start_delay": {
        "dp_id": 118,
        "code": "tank_electric_heating_start_delay",
        "raw_source": "parameter_group_1",
        "field_index": 16,
        "encoding": "int32_be",
        "step": 1,
        "name": "Tank Electric Heating Start Delay",
    },
    "heat_pump_function": {
        "dp_id": 118,
        "code": "heat_pump_function",
        "raw_source": "parameter_group_1",
        "field_index": 17,
        "encoding": "int32_be",
        "step": 1,
        "name": "Heat Pump Function",
    },
    "circulation_pump_status_after_setpoint": {
        "dp_id": 118,
        "code": "circulation_pump_status_after_setpoint",
        "raw_source": "parameter_group_1",
        "field_index": 18,
        "encoding": "int32_be",
        "step": 1,
        "name": "Circulation Pump Status After Setpoint",
    },
    "circulation_pump_onoff_cycle_after_setpoint_min": {
        "dp_id": 118,
        "code": "circulation_pump_onoff_cycle_after_setpoint_min",
        "raw_source": "parameter_group_1",
        "field_index": 19,
        "encoding": "int32_be",
        "step": 1,
        "name": "Circulation Pump On/Off Cycle After Setpoint [min]",
    },
    "dc_circulation_pump_mode": {
        "dp_id": 119,
        "code": "dc_circulation_pump_mode",
        "raw_source": "parameter_group_2",
        "field_index": 0,
        "encoding": "int32_be",
        "step": 1,
        "name": "DC Circulation Pump Mode",
    },
    "dc_water_pump_manual_speed": {
        "dp_id": 119,
        "code": "dc_water_pump_manual_speed",
        "raw_source": "parameter_group_2",
        "field_index": 1,
        "encoding": "int32_be",
        "step": 1,
        "name": "DC Water Pump Manual Speed",
        "unit": "%",
        "icon": "mdi:percent",
    },
    "delta_t_enable_units_cascade_mode": {
        "dp_id": 126,
        "code": "delta_t_enable_units_cascade_mode",
        "raw_source": "parameter_group_8",
        "field_index": 7,
        "encoding": "int32_be",
        "step": 1,
        "name": "Delta T Enable Units (Cascade Mode)",
        "unit": "°C",
        "icon": "mdi:thermometer",
        "device_class": "temperature",
    },
    "delta_t_unit_add_in_cascade_mode": {
        "dp_id": 126,
        "code": "delta_t_unit_add_in_cascade_mode",
        "raw_source": "parameter_group_8",
        "field_index": 8,
        "encoding": "int32_be",
        "step": 1,
        "name": "Delta T Unit Add (Cascade Mode)",
        "unit": "°C",
        "icon": "mdi:thermometer",
        "device_class": "temperature",
    },
    "delta_t_unit_disable_in_cascade": {
        "dp_id": 126,
        "code": "delta_t_unit_disable_in_cascade",
        "raw_source": "parameter_group_8",
        "field_index": 9,
        "encoding": "int32_be",
        "step": 1,
        "name": "Delta T Unit Disable (Cascade)",
        "unit": "°C",
        "icon": "mdi:thermometer",
        "device_class": "temperature",
    },
    "cascade_correction_cycle_sec": {
        "dp_id": 126,
        "code": "cascade_correction_cycle_sec",
        "raw_source": "parameter_group_8",
        "field_index": 10,
        "encoding": "int32_be",
        "step": 1,
        "name": "Cascade Correction Cycle [sec]",
    },
    "auto_heat_curve_max_value": {
        "dp_id": 126,
        "code": "auto_heat_curve_max_value",
        "raw_source": "parameter_group_8",
        "field_index": 11,
        "encoding": "int32_be",
        "step": 1,
        "name": "Auto Heat Curve Max Value",
        "unit": "°C",
        "icon": "mdi:thermometer",
        "device_class": "temperature",
    },
    "antifreeze_mode_dhw_operation": {
        "dp_id": 126,
        "code": "antifreeze_mode_dhw_operation",
        "raw_source": "parameter_group_8",
        "field_index": 12,
        "encoding": "int32_be",
        "step": 1,
        "name": "Antifreeze Mode (DHW Operation)",
    },
    "three_way_valve_switch_time_min": {
        "dp_id": 126,
        "code": "three_way_valve_switch_time_min",
        "raw_source": "parameter_group_8",
        "field_index": 13,
        "encoding": "int32_be",
        "step": 1,
        "name": "3-Way Valve Switch Time [min]",
    },
    "hybrid_mode_start_outdoor_temp": {
        "dp_id": 127,
        "code": "hybrid_mode_start_outdoor_temp",
        "raw_source": "parameter_group_9",
        "field_index": 3,
        "encoding": "int32_be",
        "step": 1,
        "name": "Hybrid Mode Start Outdoor Temp",
        "unit": "°C",
        "icon": "mdi:thermometer",
        "device_class": "temperature",
    },
    "hybrid_mode_delay_min": {
        "dp_id": 127,
        "code": "hybrid_mode_delay_min",
        "raw_source": "parameter_group_9",
        "field_index": 4,
        "encoding": "int32_be",
        "step": 1,
        "name": "Hybrid Mode Delay [min]",
    },
    "delta_t_setpoint_enable_hybrid_mode": {
        "dp_id": 127,
        "code": "delta_t_setpoint_enable_hybrid_mode",
        "raw_source": "parameter_group_9",
        "field_index": 5,
        "encoding": "int32_be",
        "step": 1,
        "name": "Delta T Setpoint (Enable Hybrid Mode)",
        "unit": "°C",
        "icon": "mdi:thermometer",
        "device_class": "temperature",
    },
    "energy_tariff_normal": {
        "dp_id": 127,
        "code": "energy_tariff_normal",
        "raw_source": "parameter_group_9",
        "field_index": 6,
        "encoding": "int32_be",
        "conversion": "value / 100",
        "api_conversion": "value * 100",
        "step": 1,
        "name": "Energy Tariff (Normal)",
    },
    "energy_tariff_off_peak": {
        "dp_id": 127,
        "code": "energy_tariff_off_peak",
        "raw_source": "parameter_group_9",
        "field_index": 7,
        "encoding": "int32_be",
        "conversion": "value / 100",
        "api_conversion": "value * 100",
        "step": 1,
        "name": "Energy Tariff (Off-Peak)",
    },
    "gas_price": {
        "dp_id": 127,
        "code": "gas_price",
        "raw_source": "parameter_group_9",
        "field_index": 8,
        "encoding": "int32_be",
        "conversion": "value / 100",
        "api_conversion": "value * 100",
        "step": 1,
        "name": "Gas Price",
    },
    "off_peak_start_time_weekday_hour": {
        "dp_id": 127,
        "code": "off_peak_start_time_weekday_hour",
        "raw_source": "parameter_group_9",
        "field_index": 9,
        "encoding": "int32_be",
        "step": 1,
        "name": "Off-Peak Start Time Weekday [hour]",
    },
    "off_peak_end_time_weekday": {
        "dp_id": 127,
        "code": "off_peak_end_time_weekday",
        "raw_source": "parameter_group_9",
        "field_index": 10,
        "encoding": "int32_be",
        "step": 1,
        "name": "Off-Peak End Time Weekday",
    },
    "off_peak_start_time_weekend": {
        "dp_id": 127,
        "code": "off_peak_start_time_weekend",
        "raw_source": "parameter_group_9",
        "field_index": 11,
        "encoding": "int32_be",
        "step": 1,
        "name": "Off-Peak Start Time Weekend",
    },
    "off_peak_end_time_weekend": {
        "dp_id": 127,
        "code": "off_peak_end_time_weekend",
        "raw_source": "parameter_group_9",
        "field_index": 12,
        "encoding": "int32_be",
        "step": 1,
        "name": "Off-Peak End Time Weekend",
    },
    "outdoor_temp_rise_enable_wp_pump": {
        "dp_id": 127,
        "code": "outdoor_temp_rise_enable_wp_pump",
        "raw_source": "parameter_group_9",
        "field_index": 13,
        "encoding": "int32_be",
        "step": 1,
        "name": "Outdoor Temp Rise (Enable WP Pump)",
        "unit": "°C",
        "icon": "mdi:thermometer",
        "device_class": "temperature",
    },
})

# ====================================================
# SELECT TYPES (read-write enum - accessMode: "rw")
# ====================================================
SELECT_TYPES = {
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
