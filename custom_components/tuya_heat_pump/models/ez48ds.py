"""Model mapping for Sannover Stelios 2 Heat Pump (ez48ds)."""

MODEL_NAME = "Sannover Stelios 2 Heat Pump (ez48ds)"
# ====================================================
# Sannover Stelios 2 @akemag
# ====================================================
# All entities below come directly from this device's own Tuya typeSpec
# (via tuya_api_test.py), not a guess. This is a hot water heat pump
# (tank-style water heater), not a space heating/cooling unit.
#
# temp_set (dp 4): the typeSpec gives one flat range (28-75°C), but
# Tuya's own per-mode description says Heat Pump mode actually tops out
# at 65°C, not 75°C (the other three modes do go to 75°C). The slider
# will let you set up to 75°C regardless of mode -- the device itself
# should reject/clamp a value above its real per-mode limit.
#
# A couple of dp `code` strings are misleading, same situation as seen
# on other devices sharing this Tuya template:
#   - dp 35 "temp_current_f" is NOT Fahrenheit -- typeSpec name is
#     "盘管温度" (Coil Temperature), unit is plain °C.
#   - dp 135 "return_temp" is NOT a temperature reading -- typeSpec
#     name is "回差温度" (hysteresis/differential setting), an rw
#     control value with no unit given.
#
# fault_value (dp 141): a single numeric fault code (0-255), not a
# bitmap -- Tuya gives no description of what each value means, so
# it's exposed as a raw number until a manual/translation turns up.
#
# appoint_timer (dp 139): a packed scheduling string (3 segments of 7
# characters each: on/off + hour + minute + temperature, per Tuya's
# own description). Exposed read-only as a diagnostic string rather
# than editable, since writing a malformed value could corrupt the
# device's schedule.

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
    "temp_venting": {
        "dp_id": 24,
        "code": "temp_venting",
        "name": "Discharge Temperature",
        "unit": "°C",
        "icon": "mdi:thermometer-high",
        "device_class": "temperature",
        "state_class": "measurement",
    },
    "temp_around": {
        "dp_id": 26,
        "code": "temp_around",
        "name": "Ambient Temperature",
        "unit": "°C",
        "icon": "mdi:thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
    },
    "coil_temperature": {
        "dp_id": 35,
        "code": "temp_current_f",
        "name": "Coil Temperature",
        "unit": "°C",
        "icon": "mdi:thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
    },
    "temp_return": {
        "dp_id": 102,
        "code": "temp_return",
        "name": "Return Gas Temperature",
        "unit": "°C",
        "icon": "mdi:thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
    },
    "mainboard_ver": {
        "dp_id": 111,
        "code": "mainboard_ver",
        "name": "Mainboard Version",
        "icon": "mdi:chip",
    },
    "displayboard_ver": {
        "dp_id": 112,
        "code": "displayboard_ver",
        "name": "Display Board Version",
        "icon": "mdi:chip",
    },
    "stepmotor_valve": {
        "dp_id": 113,
        "code": "stepmotor_valve",
        "name": "Expansion Valve Opening",
        "icon": "mdi:pipe-valve",
        "state_class": "measurement",
    },
    "water_recycle_temp": {
        "dp_id": 114,
        "code": "water_recycle_temp",
        "name": "Solar Collector Temperature",
        "unit": "°C",
        "icon": "mdi:solar-power",
        "device_class": "temperature",
        "state_class": "measurement",
    },
    "accumulation_times": {
        "dp_id": 116,
        "code": "accumulation_times",
        "name": "Accumulated Run Count",
        "icon": "mdi:counter",
        "state_class": "total_increasing",
    },
    "accumulation_time": {
        "dp_id": 117,
        "code": "accumulation_time",
        "name": "Accumulated Run Time",
        "icon": "mdi:timer-outline",
        "state_class": "total_increasing",
    },
    "energyconsumption": {
        "dp_id": 118,
        "code": "energyconsumption",
        "name": "Accumulated Energy Consumption",
        "unit": "kWh",
        "icon": "mdi:lightning-bolt",
        "device_class": "energy",
        "state_class": "total_increasing",
        "conversion": "value / 10",
    },
    "high_pressure": {
        "dp_id": 120,
        "code": "high_pressure",
        "name": "High Pressure",
        "icon": "mdi:gauge",
        "device_class": "pressure",
        "state_class": "measurement",
    },
    "low_pressure": {
        "dp_id": 121,
        "code": "low_pressure",
        "name": "Low Pressure",
        "icon": "mdi:gauge",
        "device_class": "pressure",
        "state_class": "measurement",
    },
    "temp_current2": {
        "dp_id": 122,
        "code": "temp_current2",
        "name": "Tank Temperature 2",
        "unit": "°C",
        "icon": "mdi:water-thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
    },
    "program_version_number": {
        "dp_id": 123,
        "code": "program_version_number",
        "name": "Program Version",
        "icon": "mdi:chip",
    },
    "fan_speed": {
        "dp_id": 124,
        "code": "fan_speed",
        "name": "Fan Speed",
        "icon": "mdi:fan",
        "state_class": "measurement",
    },
    "elec_power": {
        "dp_id": 125,
        "code": "elec_power",
        "name": "Electric Heating Power",
        "unit": "W",
        "icon": "mdi:flash",
        "device_class": "power",
        "state_class": "measurement",
    },
    "elec_runtime": {
        "dp_id": 126,
        "code": "elec_runtime",
        "name": "Electric Heating Runtime",
        "icon": "mdi:timer-outline",
        "state_class": "total_increasing",
    },
    "fan_power": {
        "dp_id": 127,
        "code": "fan_power",
        "name": "Motor Power",
        "unit": "W",
        "icon": "mdi:flash",
        "device_class": "power",
        "state_class": "measurement",
    },
    "standby_power": {
        "dp_id": 129,
        "code": "standby_power",
        "name": "Standby Power",
        "unit": "W",
        "icon": "mdi:flash",
        "device_class": "power",
        "state_class": "measurement",
    },
    "compressor_power": {
        "dp_id": 130,
        "code": "compressor_power",
        "name": "Compressor Power",
        "unit": "W",
        "icon": "mdi:flash",
        "device_class": "power",
        "state_class": "measurement",
    },
    "electrovalve_angle": {
        "dp_id": 137,
        "code": "electrovalve_angle",
        "name": "Electronic Expansion Valve Opening",
        "icon": "mdi:pipe-valve",
        "state_class": "measurement",
    },
    # See header note -- packed scheduling string, read-only.
    "appoint_timer": {
        "dp_id": 139,
        "code": "appoint_timer",
        "name": "Scheduled Timer (Raw)",
        "icon": "mdi:timer-cog-outline",
    },
    "fault_value": {
        "dp_id": 141,
        "code": "fault_value",
        "name": "Fault Value",
        "icon": "mdi:alert-circle",
    },
}

BINARY_SENSOR_TYPES = {
    "compressor_state": {
        "dp_id": 27,
        "code": "compressor_state",
        "name": "Compressor Status",
        "device_class": "running",
    },
    "four_valve_state": {
        "dp_id": 28,
        "code": "four_valve_state",
        "name": "4-Way Valve Status",
        "icon": "mdi:valve",
    },
    "draught_fan_state": {
        "dp_id": 29,
        "code": "draught_fan_state",
        "name": "Fan High Speed Status",
        "icon": "mdi:fan",
    },
    "pump_state": {
        "dp_id": 30,
        "code": "pump_state",
        "name": "Circulation Pump Status",
        "device_class": "running",
    },
    "ele_heating_state": {
        "dp_id": 32,
        "code": "ele_heating_state",
        "name": "Electric Heating Status",
        "device_class": "heat",
    },
    "defrost_state": {
        "dp_id": 33,
        "code": "defrost_state",
        "name": "Defrost Active",
        "device_class": "heat",
    },
    "solar_state": {
        "dp_id": 103,
        "code": "solar_state",
        "name": "Solar/PV Status",
        "icon": "mdi:solar-power",
    },
    "water_recycle_state": {
        "dp_id": 104,
        "code": "water_recycle_state",
        "name": "Solar Water Pump Status",
        "device_class": "running",
    },
    "draught_fan_state2": {
        "dp_id": 107,
        "code": "draught_fan_state2",
        "name": "Fan Low Speed Status",
        "icon": "mdi:fan",
    },
    "disinfect_state": {
        "dp_id": 109,
        "code": "disinfect_state",
        "name": "Disinfection Status",
        "icon": "mdi:bacteria-outline",
    },
    "antifreeze_state": {
        "dp_id": 110,
        "code": "antifreeze_state",
        "name": "Antifreeze Status",
        "icon": "mdi:snowflake-alert",
    },
    "appiontment_state": {
        "dp_id": 142,
        "code": "appiontment_state",
        "name": "Timer Active",
        "icon": "mdi:timer-outline",
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
    "disinfection": {
        "dp_id": 9,
        "code": "disinfection",
        "name": "Disinfection Function",
        "icon": "mdi:bacteria-outline",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']",
    },
    "e_anode_enable": {
        "dp_id": 101,
        "code": "e_anode_enable",
        "name": "Electronic Anode Function",
        "icon": "mdi:lightning-bolt-outline",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']",
    },
    "water_recycle_enable": {
        "dp_id": 105,
        "code": "water_recycle_enable",
        "name": "Solar Circulation Function",
        "icon": "mdi:solar-power",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']",
    },
    "solar_enable": {
        "dp_id": 106,
        "code": "solar_enable",
        "name": "Solar/PV Function",
        "icon": "mdi:solar-power",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']",
    },
    "antifreeze_enable": {
        "dp_id": 108,
        "code": "antifreeze_enable",
        "name": "Antifreeze Function",
        "icon": "mdi:snowflake",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']",
    },
    "backpump_state": {
        "dp_id": 115,
        "code": "backpump_state",
        "name": "Tank Circulation Function",
        "icon": "mdi:pump",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']",
    },
    "holiday_enable": {
        "dp_id": 119,
        "code": "holiday_enable",
        "name": "Holiday Mode",
        "icon": "mdi:beach",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']",
    },
    "power_outage_memory": {
        "dp_id": 128,
        "code": "power_outage_memory",
        "name": "Power Outage Memory",
        "icon": "mdi:memory",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']",
    },
}

NUMBER_TYPES = {
    # See header note -- real max depends on mode (Heat Pump mode tops
    # out at 65°C per Tuya's own description, others at 75°C).
    "temp_set": {
        "dp_id": 4,
        "code": "temp_set",
        "name": "Target Temperature",
        "icon": "mdi:thermostat",
        "unit": "°C",
        "min_value": 28.0,
        "max_value": 75.0,
        "step": 1.0,
        "api_conversion": "value",
    },
    "defrost_end_temp": {
        "dp_id": 131,
        "code": "defrost_end_temp",
        "name": "Defrost End Temperature",
        "icon": "mdi:thermometer",
        "unit": "°C",
        "min_value": 0.0,
        "max_value": 65535.0,
        "step": 1.0,
        "api_conversion": "value",
    },
    "defrost_interval": {
        "dp_id": 132,
        "code": "defrost_interval",
        "name": "Defrost Interval",
        "icon": "mdi:timer-cog-outline",
        "min_value": 0.0,
        "max_value": 65535.0,
        "step": 1.0,
        "api_conversion": "value",
    },
    "defrost_runtime": {
        "dp_id": 133,
        "code": "defrost_runtime",
        "name": "Defrost Runtime",
        "icon": "mdi:timer-cog-outline",
        "min_value": 0.0,
        "max_value": 65535.0,
        "step": 1.0,
        "api_conversion": "value",
    },
    "tank_temp_compensation": {
        "dp_id": 134,
        "code": "tank_temp_compensation",
        "name": "Tank Temperature Compensation",
        "icon": "mdi:thermometer",
        "unit": "°C",
        "min_value": -5.0,
        "max_value": 99.0,
        "step": 1.0,
        "api_conversion": "value",
    },
    # Hysteresis/differential setting, not a temperature reading -- see
    # header note.
    "return_temp": {
        "dp_id": 135,
        "code": "return_temp",
        "name": "Hysteresis Temperature",
        "icon": "mdi:thermometer",
        "min_value": 0.0,
        "max_value": 65535.0,
        "step": 1.0,
        "api_conversion": "value",
    },
    "defrost_start_temp": {
        "dp_id": 136,
        "code": "defrost_start_temp",
        "name": "Defrost Start Temperature",
        "icon": "mdi:thermometer",
        "unit": "°C",
        "min_value": -10.0,
        "max_value": 99.0,
        "step": 1.0,
        "api_conversion": "value",
    },
    "disinfect_runtime": {
        "dp_id": 138,
        "code": "disinfect_runtime",
        "name": "Disinfection Runtime",
        "icon": "mdi:timer-cog-outline",
        "min_value": 0.0,
        "max_value": 65535.0,
        "step": 1.0,
        "api_conversion": "value",
    },
    "holiday_days": {
        "dp_id": 140,
        "code": "holiday_days",
        "name": "Holiday Days",
        "icon": "mdi:beach",
        "unit": "days",
        "min_value": 0.0,
        "max_value": 99.0,
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
            "0x00": "Auto",
            "0x01": "Electric Heating",
            "0x02": "Heat Pump",
            "0x03": "Rapid Heating",
        },
    },
}
