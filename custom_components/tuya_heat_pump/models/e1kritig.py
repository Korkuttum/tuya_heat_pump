# ====================================================
# Smad Monobloc 12kW @reneruault-code, issue #115
# Tuya modelId: e1kritig
# Air-to-water monobloc heat pump with two heating zones,
# two cooling zones and a hot water function.
#
# NOT decoded yet (raw data points, need the raw explorer):
#   - all_6d_data (dp 145): the full status report. The live
#     temperatures (water in/out, outdoor, tank, ...) are most
#     likely inside it, which is why temp_current (dp 16) reads
#     -30 (the minimum, i.e. "no value") in the reported dump.
#   - error_warning (dp 146): fault / warning bits.
#   - gr_set_vac_date, gr_zone1_schedule_ctr, gr_zone2_schedule_ctr,
#     gr_hot_water_schedule_ctr, sterilization_time (dp 125-128, 136):
#     schedule and date tables.
#   - engineering_parameters / engineering_operation (dp 198, 199):
#     service menu, deliberately not exposed.
#
# Not exposed on purpose:
#   - temp_current_f (dp 35): Fahrenheit twin of temp_current.
#   - callback_sysadjust (dp 197): firmware update result code.
#   - schedule_time_weeks (dp 151): belongs to the raw schedules.
#
# Ranges: the cloud schema only says 0-210 for every setpoint,
# so the limits below are cautious values taken from the unit's
# published operating range. None of them is confirmed on a unit.
# ====================================================
"""Model mapping for Smad Monobloc 12kW (e1kritig)."""

MODEL_NAME = "Smad Monobloc 12kW (e1kritig)"

# Sensor Types
SENSOR_TYPES = {
    "temp_current": {
        # Reads -30 (the schema minimum) while the unit is off, so most
        # likely "no value". Kept to see what it shows on a running unit.
        "dp_id": 16,
        "code": "temp_current",
        "name": "Current Temperature",
        "unit": "°C",
        "icon": "mdi:thermometer",
        "device_class": "temperature",
        "state_class": "measurement",
    },
}

# Binary Sensor Types
BINARY_SENSOR_TYPES = {}

# Switch Types - read-write booleans
SWITCH_TYPES = {
    "switch": {
        "dp_id": 1,
        "code": "switch",
        "name": "Power",
        "icon": "mdi:power",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']",
    },
    "heater_zone1_switch": {
        "dp_id": 101,
        "code": "heater_zone1_switch",
        "name": "Heating Zone 1",
        "icon": "mdi:radiator",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']",
    },
    "heater_zone2_switch": {
        "dp_id": 102,
        "code": "heater_zone2_switch",
        "name": "Heating Zone 2",
        "icon": "mdi:radiator",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']",
    },
    "cold_zone1_switch": {
        "dp_id": 103,
        "code": "cold_zone1_switch",
        "name": "Cooling Zone 1",
        "icon": "mdi:snowflake",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']",
    },
    "cold_zone2_switch": {
        "dp_id": 104,
        "code": "cold_zone2_switch",
        "name": "Cooling Zone 2",
        "icon": "mdi:snowflake",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']",
    },
    "hot_water_mode_switch": {
        "dp_id": 115,
        "code": "hot_water_mode_switch",
        "name": "Hot Water Mode",
        "icon": "mdi:water-boiler",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']",
    },
    "zcw_single_cycle_status": {
        "dp_id": 132,
        "code": "zcw_single_cycle_status",
        "name": "Zero Cold Water Single Cycle",
        "icon": "mdi:water-sync",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']",
    },
    "sterilization_status": {
        "dp_id": 138,
        "code": "sterilization_status",
        "name": "Sterilization",
        "icon": "mdi:shield-check",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']",
    },
    "disinfect_status_mon": {
        "dp_id": 147,
        "code": "disinfect_status_mon",
        "name": "Sterilization Monday",
        "icon": "mdi:calendar-check",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']",
    },
    "disinfect_status_tue": {
        "dp_id": 144,
        "code": "disinfect_status_tue",
        "name": "Sterilization Tuesday",
        "icon": "mdi:calendar-check",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']",
    },
    "disinfect_status_wed": {
        "dp_id": 143,
        "code": "disinfect_status_wed",
        "name": "Sterilization Wednesday",
        "icon": "mdi:calendar-check",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']",
    },
    "disinfect_status_thu": {
        "dp_id": 142,
        "code": "disinfect_status_thu",
        "name": "Sterilization Thursday",
        "icon": "mdi:calendar-check",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']",
    },
    "disinfect_status_fri": {
        "dp_id": 141,
        "code": "disinfect_status_fri",
        "name": "Sterilization Friday",
        "icon": "mdi:calendar-check",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']",
    },
    "disinfect_status_sat": {
        "dp_id": 140,
        "code": "disinfect_status_sat",
        "name": "Sterilization Saturday",
        "icon": "mdi:calendar-check",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']",
    },
    "disinfect_status_sun": {
        "dp_id": 139,
        "code": "disinfect_status_sun",
        "name": "Sterilization Sunday",
        "icon": "mdi:calendar-check",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']",
    },
    "mute_status": {
        "dp_id": 148,
        "code": "mute_status",
        "name": "Silent Mode",
        "icon": "mdi:volume-off",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']",
    },
    "boost": {
        "dp_id": 149,
        "code": "boost",
        "name": "Boost",
        "icon": "mdi:rocket-launch",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']",
    },
    "vac_mode": {
        "dp_id": 150,
        "code": "vac_mode",
        "name": "Vacation Mode",
        "icon": "mdi:beach",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']",
    },
    "timing_on_off_status": {
        "dp_id": 179,
        "code": "timing_on_off_status",
        "name": "Timer On/Off",
        "icon": "mdi:timer-outline",
        "conversion": "value in [1, True, '1', 'true', 'on', 'yes', 'enable', 'open']",
    },
}

# Number Types - read-write values
NUMBER_TYPES = {
    "temp_set": {
        "dp_id": 4,
        "code": "temp_set",
        "name": "Hot Water Target Temperature",
        "icon": "mdi:water-thermometer",
        "unit": "°C",
        "min_value": 30.0,
        "max_value": 60.0,
        "step": 1.0,
        "api_conversion": "value",
    },
    "heating_zone1_target_temp": {
        "dp_id": 105,
        "code": "heating_zone1_target_temp",
        "name": "Heating Zone 1 Target Temperature",
        "icon": "mdi:thermometer",
        "unit": "°C",
        "min_value": 20.0,
        "max_value": 75.0,
        "step": 1.0,
        "api_conversion": "value",
    },
    "heating_zone2_target_temp": {
        "dp_id": 106,
        "code": "heating_zone2_target_temp",
        "name": "Heating Zone 2 Target Temperature",
        "icon": "mdi:thermometer",
        "unit": "°C",
        "min_value": 20.0,
        "max_value": 75.0,
        "step": 1.0,
        "api_conversion": "value",
    },
    "cold_zone1_target_temp": {
        "dp_id": 107,
        "code": "cold_zone1_target_temp",
        "name": "Cooling Zone 1 Target Temperature",
        "icon": "mdi:thermometer",
        "unit": "°C",
        "min_value": 5.0,
        "max_value": 25.0,
        "step": 1.0,
        "api_conversion": "value",
    },
    "cold_zone2_target_temp": {
        "dp_id": 108,
        "code": "cold_zone2_target_temp",
        "name": "Cooling Zone 2 Target Temperature",
        "icon": "mdi:thermometer",
        "unit": "°C",
        "min_value": 5.0,
        "max_value": 25.0,
        "step": 1.0,
        "api_conversion": "value",
    },
    "steriliz_retention_time": {
        "dp_id": 134,
        "code": "steriliz_retention_time",
        "name": "Sterilization Hold Time",
        "icon": "mdi:timer-sand",
        "unit": "min",
        "min_value": 0.0,
        "max_value": 99.0,
        "step": 1.0,
        "api_conversion": "value",
    },
    "steri_temperature": {
        "dp_id": 137,
        "code": "steri_temperature",
        "name": "Sterilization Temperature",
        "icon": "mdi:thermometer-high",
        "unit": "°C",
        "min_value": 50.0,
        "max_value": 75.0,
        "step": 1.0,
        "api_conversion": "value",
    },
}

# Select Types - read-write enums. The unit only publishes the values
# 0 / 1 / 2, their meaning is not known yet.
SELECT_TYPES = {
    "heating_sub_mode": {
        # Reads 1 on the reported unit.
        "dp_id": 129,
        "code": "heating_sub_mode",
        "name": "Heating Sub Mode",
        "icon": "mdi:cog",
        "options": {
            "0": "Mode 0",
            "1": "Mode 1",
            "2": "Mode 2",
        },
    },
    "hot_water_sub_mode": {
        # Reads 0 on the reported unit.
        "dp_id": 133,
        "code": "hot_water_sub_mode",
        "name": "Hot Water Sub Mode",
        "icon": "mdi:cog",
        "options": {
            "0": "Mode 0",
            "1": "Mode 1",
            "2": "Mode 2",
        },
    },
    "t_zone2_heat_ope_sub": {
        # Reads 0 on the reported unit.
        "dp_id": 176,
        "code": "t_zone2_heat_ope_sub",
        "name": "Zone 2 Heating Sub Mode",
        "icon": "mdi:cog",
        "options": {
            "0": "Mode 0",
            "1": "Mode 1",
            "2": "Mode 2",
        },
    },
}
