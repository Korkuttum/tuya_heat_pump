"""Model mapping for Ecolynx Heat Pump (e1ms13ng)."""

MODEL_NAME = "Ecolynx Heat Pump (e1ms13ng)"
# ====================================================
# Ecolynx @bxbxbx
# ====================================================
# Rebranded R290 heat pump sold in Germany as "Ecolynx" (reporter
# suspects original manufacturer Micoe or Sacon). All entities below
# come directly from this device's own Tuya typeSpec (via
# tuya_api_test.py), not a guess.
#
# IMPORTANT — several dp `code` strings are misleading on this device.
# Tuya's generic template reuses the same dp_id/code across many
# products, and this manufacturer repurposed some of them without
# renaming the code, so always trust the typeSpec's own Chinese name
# and unit over the code string:
#   - dp 16 "temp_current" is NOT a temperature -- typeSpec name is
#     "主阀" (Main Valve), unit "P" (position), range -500..500.
#   - dp 25 "effluent_temp" is NOT a temperature -- typeSpec name is
#     "辅阀" (Auxiliary Valve), same unit/range as dp 16.
#   - dp 39 "venting_temp_f" is NOT a temperature -- typeSpec name is
#     "水流量" (Water Flow Rate), unit "L/min".
#   - dp 40 "effluent_temp_f" is NOT a temperature -- typeSpec name is
#     "风机频率" (Fan Frequency), unit "Hz".
#   - dp 36 "top_temp_f" genuinely IS in Fahrenheit per its own
#     typeSpec (unit "℉") -- typeSpec name "低压饱和温度" (Low
#     Pressure Saturation Temperature). Every other "_f"-suffixed code
#     on this device is actually Celsius despite the suffix.
#
# fault (dp 15): Tuya's own bitmap labels are just "1".."30" with no
# text -- no manufacturer fault-code manual available yet, so this is
# exposed as a raw bitmap number plus a simple problem/no-problem
# binary sensor until someone can supply the real descriptions.
#
# water_set (dp 10, range 0-1, unit "L") and volume_set (dp 106, range
# 0-2) don't have a clear end-user meaning from the schema alone --
# volume_set's own (Chinese) description says 0=no metering module,
# 1=single-phase, 2=three-phase, so it's likely an installer/config
# option rather than something to change day-to-day. Exposed as plain
# numbers rather than guessed selects.
#
# syscomp/threemode/fourmode/autotype (dp 113-116): multi-system/
# cascade configuration -- present on this unit's schema but not
# obviously relevant to a single stand-alone install. Exposed as-is
# since the schema offers them; feel free to ignore if not applicable.

SENSOR_TYPES = {
    "fault": {
        "dp_id": 15,
        "code": "fault",
        "name": "Fault Bitmap",
        "icon": "mdi:alert-circle",
    },
    "main_valve_position": {
        "dp_id": 16,
        "code": "temp_current",
        "name": "Main Valve Position",
        "unit": "P",
        "icon": "mdi:pipe-valve",
        "state_class": "measurement",
    },
    "power_consumption_today": {
        "dp_id": 18,
        "code": "power_consumption",
        "name": "Power Consumption Today",
        "unit": "kWh",
        "icon": "mdi:lightning-bolt",
        "device_class": "energy",
        "state_class": "total_increasing",
        "conversion": "value / 100",
    },
    "compressor_frequency": {
        "dp_id": 20,
        "code": "compressor_strength",
        "name": "Compressor Frequency",
        "unit": "Hz",
        "icon": "mdi:sine-wave",
        "device_class": "frequency",
        "state_class": "measurement",
    },
    "water_inlet_temperature": {
        "dp_id": 21,
        "code": "temp_top",
        "name": "Water Inlet Temperature",
        "unit": "°C",
        "icon": "mdi:water-thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
    },
    "water_outlet_temperature": {
        "dp_id": 22,
        "code": "temp_bottom",
        "name": "Water Outlet Temperature",
        "unit": "°C",
        "icon": "mdi:water-thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
    },
    "coil_temperature": {
        "dp_id": 23,
        "code": "coiler_temp",
        "name": "Coil Temperature",
        "unit": "°C",
        "icon": "mdi:thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
    },
    "discharge_temperature": {
        "dp_id": 24,
        "code": "venting_temp",
        "name": "Discharge Temperature",
        "unit": "°C",
        "icon": "mdi:thermometer-high",
        "device_class": "temperature",
        "state_class": "measurement",
    },
    "auxiliary_valve_position": {
        "dp_id": 25,
        "code": "effluent_temp",
        "name": "Auxiliary Valve Position",
        "unit": "P",
        "icon": "mdi:pipe-valve",
        "state_class": "measurement",
    },
    "ambient_temperature": {
        "dp_id": 26,
        "code": "around_temp",
        "name": "Ambient Temperature",
        "unit": "°C",
        "icon": "mdi:thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
    },
    "high_pressure_saturation_temperature": {
        "dp_id": 35,
        "code": "temp_current_f",
        "name": "High Pressure Saturation Temperature",
        "unit": "°C",
        "icon": "mdi:thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
    },
    "low_pressure_saturation_temperature": {
        "dp_id": 36,
        "code": "top_temp_f",
        "name": "Low Pressure Saturation Temperature",
        "unit": "°F",
        "icon": "mdi:thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
    },
    "inner_coil_temperature": {
        "dp_id": 37,
        "code": "bottom_temp_f",
        "name": "Inner Coil Temperature",
        "unit": "°C",
        "icon": "mdi:thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
    },
    "water_tank_temperature": {
        "dp_id": 38,
        "code": "around_temp_f",
        "name": "Water Tank Temperature",
        "unit": "°C",
        "icon": "mdi:water-thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
    },
    "water_flow_rate": {
        "dp_id": 39,
        "code": "venting_temp_f",
        "name": "Water Flow Rate",
        "unit": "L/min",
        "icon": "mdi:water-pump",
        "state_class": "measurement",
    },
    "fan_frequency": {
        "dp_id": 40,
        "code": "effluent_temp_f",
        "name": "Fan Frequency",
        "unit": "Hz",
        "icon": "mdi:fan",
        "device_class": "frequency",
        "state_class": "measurement",
    },
    "return_gas_temperature": {
        "dp_id": 41,
        "code": "coiler_temp_f",
        "name": "Return Gas Temperature",
        "unit": "°C",
        "icon": "mdi:thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
    },
    "phase_a_current": {
        "dp_id": 102,
        "code": "cur_current",
        "name": "Phase A Current",
        "unit": "A",
        "icon": "mdi:current-ac",
        "device_class": "current",
        "state_class": "measurement",
        "conversion": "value / 1000",
    },
    "phase_a_voltage": {
        "dp_id": 103,
        "code": "voltage_current",
        "name": "Phase A Voltage",
        "unit": "V",
        "icon": "mdi:flash",
        "device_class": "voltage",
        "state_class": "measurement",
        "conversion": "value / 10",
    },
    "power": {
        "dp_id": 104,
        "code": "cur_power",
        "name": "Power",
        "unit": "W",
        "icon": "mdi:flash",
        "device_class": "power",
        "state_class": "measurement",
        "conversion": "value / 10",
    },
    "total_energy": {
        "dp_id": 105,
        "code": "electric_total",
        "name": "Total Energy",
        "unit": "kWh",
        "icon": "mdi:lightning-bolt",
        "device_class": "energy",
        "state_class": "total_increasing",
        "conversion": "value / 100",
    },
    "economizer_inlet_temperature": {
        "dp_id": 107,
        "code": "eviin",
        "name": "Economizer Inlet Temperature",
        "unit": "°C",
        "icon": "mdi:thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
    },
    "economizer_outlet_temperature": {
        "dp_id": 108,
        "code": "eviout",
        "name": "Economizer Outlet Temperature",
        "unit": "°C",
        "icon": "mdi:thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
    },
    "phase_b_current": {
        "dp_id": 109,
        "code": "b_cur",
        "name": "Phase B Current",
        "unit": "A",
        "icon": "mdi:current-ac",
        "device_class": "current",
        "state_class": "measurement",
        "conversion": "value / 1000",
    },
    "phase_c_current": {
        "dp_id": 110,
        "code": "c_cur",
        "name": "Phase C Current",
        "unit": "A",
        "icon": "mdi:current-ac",
        "device_class": "current",
        "state_class": "measurement",
        "conversion": "value / 1000",
    },
    "phase_b_voltage": {
        "dp_id": 111,
        "code": "bv",
        "name": "Phase B Voltage",
        "unit": "V",
        "icon": "mdi:flash",
        "device_class": "voltage",
        "state_class": "measurement",
        "conversion": "value / 10",
    },
    "phase_c_voltage": {
        "dp_id": 112,
        "code": "cv",
        "name": "Phase C Voltage",
        "unit": "V",
        "icon": "mdi:flash",
        "device_class": "voltage",
        "state_class": "measurement",
        "conversion": "value / 10",
    },
    # Mainboard program/diagnostic register -- Tuya's own description
    # notes different ranges mean different mode counts (7-mode vs
    # 4-mode firmware), not something end users act on directly.
    "mainboard_program": {
        "dp_id": 14,
        "code": "countdown_left",
        "name": "Mainboard Program",
        "icon": "mdi:counter",
        "state_class": "measurement",
    },
}

BINARY_SENSOR_TYPES = {
    "fault": {
        "dp_id": 15,
        "code": "fault",
        "name": "Fault Status",
        "device_class": "problem",
        "conversion": "value != 0",
    },
    "cooling_mode_active": {
        "dp_id": 27,
        "code": "compressor_state",
        "name": "Cooling Mode Active",
        "icon": "mdi:snowflake",
    },
    "hot_water_mode_active": {
        "dp_id": 31,
        "code": "backwater",
        "name": "Hot Water Mode Active",
        "icon": "mdi:water-boiler",
    },
    "defrost": {
        "dp_id": 33,
        "code": "defrost_state",
        "name": "Defrost Active",
        "device_class": "heat",
    },
}

SWITCH_TYPES = {
    "switch": {
        "dp_id": 1,
        "code": "switch",
        "name": "Power",
        "icon": "mdi:power",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']",
    },
}

NUMBER_TYPES = {
    "temp_set": {
        "dp_id": 4,
        "code": "temp_set",
        "name": "Target Temperature",
        "icon": "mdi:thermostat",
        "unit": "°C",
        "min_value": 5.0,
        "max_value": 80.0,
        "step": 1.0,
        "api_conversion": "value",
    },
    "hot_water_setpoint": {
        "dp_id": 101,
        "code": "minitemp_set",
        "name": "Hot Water Setpoint (Combined Mode)",
        "icon": "mdi:water-thermometer",
        "unit": "°C",
        "min_value": 5.0,
        "max_value": 80.0,
        "step": 1.0,
        "api_conversion": "value",
    },
    # See header note -- meaning not fully confirmed from the schema alone.
    "water_volume_setting": {
        "dp_id": 10,
        "code": "water_set",
        "name": "Water Volume Setting",
        "icon": "mdi:water",
        "unit": "L",
        "min_value": 0.0,
        "max_value": 1.0,
        "step": 1.0,
        "api_conversion": "value",
    },
    # 0 = no metering module, 1 = single-phase, 2 = three-phase (per
    # Tuya's own description) -- installer/config option.
    "power_metering_module": {
        "dp_id": 106,
        "code": "volume_set",
        "name": "Power Metering Module",
        "icon": "mdi:meter-electric",
        "min_value": 0.0,
        "max_value": 2.0,
        "step": 1.0,
        "api_conversion": "value",
    },
}

SELECT_TYPES = {
    "mode": {
        "dp_id": 2,
        "code": "mode",
        "name": "Mode",
        "icon": "mdi:hvac",
        "options": {
            "cold": "Cooling",
            "heating": "Heating",
            "hot_water": "Hot Water",
            "cold_and_hotwater": "Cooling + Hot Water",
            "heating_and_hot_water": "Heating + Hot Water",
            "auto": "Auto",
            "auto_and_hotwater": "Auto + Hot Water",
        },
    },
    "work_mode": {
        "dp_id": 5,
        "code": "work_mode",
        "name": "Work Mode",
        "icon": "mdi:cog",
        "options": {
            "ECO": "Eco",
            "Normal": "Normal",
            "Boost": "Boost",
        },
    },
    "hot_water_curve": {
        "dp_id": 11,
        "code": "capacity_set",
        "name": "Hot Water Curve",
        "icon": "mdi:chart-bell-curve",
        "options": {
            "OFF": "Off",
            "H1": "H1",
            "H2": "H2",
            "H3": "H3",
            "H4": "H4",
        },
    },
    "heating_curve": {
        "dp_id": 13,
        "code": "countdown_set",
        "name": "Heating Curve",
        "icon": "mdi:chart-bell-curve",
        "options": {
            "OFF": "Off",
            "H1": "H1", "H2": "H2", "H3": "H3", "H4": "H4",
            "H5": "H5", "H6": "H6", "H7": "H7", "H8": "H8",
            "L1": "L1", "L2": "L2", "L3": "L3", "L4": "L4",
            "L5": "L5", "L6": "L6", "L7": "L7", "L8": "L8",
        },
    },
    # Multi-system/cascade configuration -- see header note.
    "system_count": {
        "dp_id": 113,
        "code": "syscomp",
        "name": "Number of Systems",
        "icon": "mdi:counter",
        "options": {
            "0": "0",
            "1": "1",
        },
    },
    "system_selection": {
        "dp_id": 114,
        "code": "threemode",
        "name": "System Selection",
        "icon": "mdi:counter",
        "options": {
            "1": "System 1",
            "2": "System 2",
        },
    },
    "secondary_mode": {
        "dp_id": 115,
        "code": "fourmode",
        "name": "Secondary System Mode",
        "icon": "mdi:hvac",
        "options": {
            "Cool": "Cooling",
            "Heat": "Heating",
            "Auto": "Auto",
        },
    },
    "auto_mode_bias": {
        "dp_id": 116,
        "code": "autotype",
        "name": "Auto Mode Bias",
        "icon": "mdi:autorenew",
        "options": {
            "C": "Cooling-biased",
            "H": "Heating-biased",
        },
    },
}
